import uuid
from uuid import uuid4

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from user.object_managers import MediatorManager, OnlyBasicUserManager
from utils.common import sample_queryset

NULLABLE = {'blank': True, 'null': True}


class Statuses(models.TextChoices):
    NEW = "New"
    APPROVED = "Approved"
    BLOCKED = "Blocked"
    DECLINED = "Declined"


class User(PermissionsMixin, AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_("ID пользователя"))
    firstname = models.CharField(max_length=150, **NULLABLE, verbose_name=_("Имя"))
    lastname = models.CharField(max_length=150, **NULLABLE, verbose_name=_("Фамилия"))
    email = models.CharField(max_length=150, null=False, blank=False, unique=True, verbose_name=_("email"))
    phone = models.CharField(max_length=12, **NULLABLE, verbose_name=_("Телефон"))
    birthday = models.DateField(**NULLABLE, verbose_name=_("День рождения"))
    create_at = models.DateTimeField(auto_now_add=True, **NULLABLE, verbose_name=_("Создан"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активный"))
    is_staff = models.BooleanField(default=False, verbose_name=_("Сотрудник"))
    is_superuser = models.BooleanField(default=False, verbose_name=_("superuser"))   
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True, verbose_name=_("Аватарка"))
    status = models.TextField(
        verbose_name="Статус",
        choices=Statuses.choices,
        default=Statuses.NEW,
        null=False,
        blank=False,
    )
    deleted = models.BooleanField(default=False, verbose_name=_("Удален"))
    deleted_at = models.DateTimeField(null=True, verbose_name=_("Дата удаления"))

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    def __str__(self):
        return f'{self.firstname} {self.lastname}, {self.email}'

    def average_rating(self):
        """Вывод среднего рейтинга медиатора"""
        rating = self.reviews.aggregate(avg_rating=models.Avg('rating'))[
            'avg_rating']
        if rating is None:
            return 0.0
        return round(rating, 1)

    def top3_mediator_list(self):
        """Тут выборка из всех медиаторов. Надо бы посчитать рейтинг, потом как-нибудь"""
        # k = min(Mediator.objects.count(), 3)
        # return sample(list(Mediator.objects.all()), k=k)
        return sample_queryset(Mediator, 3)

    def conflicts_new(self):
        """Вернет количество конфликтов, у которых статус 'Новый'"""
        return self.created_conflicts.filter(status='Новый').count()

    def conflicts_in_work(self):
        """Вернет количество конфликтов, у которых статус 'В работе'"""
        return self.created_conflicts.filter(status='В работе').count()

    def conflicts_completed(self):
        """Вернет количество конфликтов, у которых статус 'Завершен'"""
        return self.created_conflicts.filter(status='Завершен').count()

    # def get_absolute_url(self):
    #     return reverse('post', kwargs={'post_id': self.pk})

    class Meta:
        verbose_name = _("Прользователь")
        verbose_name_plural = _("Прользователи")


class EmailConfirmation(models.Model):
    user = models.OneToOneField(
        User,
        related_name="email_confirmation",
        verbose_name="email подтверждена",
        on_delete=models.DO_NOTHING,
    )
    approval_code = models.CharField(
        max_length=128,
        verbose_name='Код подтверждения',
        unique=True,
    )
    code_expiration_date = models.DateTimeField(
        verbose_name='Дата истечения срока действия кода')
    is_approved = models.BooleanField(verbose_name='Approved?', default=False)

    class Meta:
        verbose_name = _("Подтверждение почты")
        verbose_name_plural = _("Подтверждение почты")


class BasicUser(User):
    objects = OnlyBasicUserManager()

    class Meta:
        proxy = True
        verbose_name = _("Клиент")
        verbose_name_plural = _("Клиенты")


class Mediator(User):
    objects = MediatorManager()

    class Meta:
        ordering = ['create_at']
        proxy = True
        verbose_name = _("Медиатор")
        verbose_name_plural = _("Медиаторы")


class AdditionalInfo(Mediator):
    mediator = models.OneToOneField(
        Mediator,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='get_info',
        verbose_name=_("Медиатор")
    )
    rate = models.IntegerField(blank=True, null=True, verbose_name = _("Ставка"))
    description = models.TextField(blank=True, null=True, verbose_name = _("Описание"))

    class Meta:
        verbose_name = _("Дополнительная информация")
        verbose_name_plural = _("Дополнительная информация")



class ContactMessage(models.Model):
    create_at = models.DateTimeField(auto_now_add=True,
                                     verbose_name=_("Создан"))
    name = models.CharField(max_length=150, null=False, blank=False, verbose_name=_("Имя"))
    email = models.EmailField(max_length=150, null=False, blank=False,
                              verbose_name=_("Email"))
    message = models.TextField(
        null=False, blank=False,
        max_length=500,
        error_messages={
            'required': 'Пожалуйста, заполните это поле.',
            'invalid': 'Напишите нам сообщение.',
        },
        verbose_name=_(
         "Сообщения пользователей"))

    class Meta:
        ordering = ['-create_at']
        verbose_name = _("Сообщения пользователей")
        verbose_name_plural = _("Сообщения пользователей")


class UserMessage(models.Model):
    """
    Модель для сообщений в личной переписке
    """
    id = models.UUIDField(primary_key=True, default=uuid4, verbose_name=_("ID сообщения"))

    from_user = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  related_name='user_from',
                                  verbose_name=_("От пользователя")
                                  )
    to_user = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='user_to',
                                verbose_name=_("Для пользователя")
                                )
    message_time = models.DateTimeField(auto_now_add=True,
                                        editable=False,
                                        verbose_name=_("Время сообщения"))
    message = models.TextField(
        max_length=1000,
        verbose_name=_(
            "Сообщение")
    )
    class Meta:
        ordering = ['-message_time']
        verbose_name = _("Сообщение в конфликте")
        verbose_name_plural = _("Сообщения в конфликте")


class ContactUser(models.Model):
    """
    Модель для контактов пользователя
    """
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='user_to_contact',
                             verbose_name=_("От пользователя")
                             )
    contact = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='user_contact',
                                verbose_name=_("От пользователя")
                                )
    new_messages = models.BooleanField(default=False, verbose_name=_("Есть новые сообщения"))
    last_message_time = models.DateTimeField(auto_now_add=True,
                                             verbose_name=_("Время последнего сообщения"))

    class Meta:
        ordering = ['-last_message_time']
        verbose_name = _("Контакт пользлвателя")
        verbose_name_plural = _("Контакты пользлвателя")

