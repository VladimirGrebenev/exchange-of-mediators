from utils.common import sample_queryset

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
import uuid

from user.object_managers import MediatorManager, OnlyBasicUserManager

NULLABLE = {'blank': True, 'null': True}


class Statuses(models.TextChoices):
    NEW = "New"
    APPROVED = "Approved"
    BLOCKED = "Blocked"
    DECLINED = "Declined"


class User(PermissionsMixin, AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstname = models.CharField(max_length=150, **NULLABLE)
    lastname = models.CharField(max_length=150, **NULLABLE)
    email = models.CharField(max_length=150, null=False, blank=False, unique=True)
    phone = models.CharField(max_length=12, **NULLABLE)
    birthday = models.DateField(**NULLABLE)
    create_at = models.DateTimeField(auto_now_add=True, **NULLABLE)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    status = models.TextField(
        verbose_name="status",
        choices=Statuses.choices,
        default=Statuses.NEW,
        null=False,
        blank=False,
    )
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    def __str__(self):
        return f'{self.firstname} {self.lastname}, {self.email}'

    def average_rating(self):
        """Вывод среднего рейтинга медиатора"""
        rating = self.reviews.aggregate(avg_rating=models.Avg('rating'))['avg_rating']
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


class EmailConfirmation(models.Model):
    user = models.OneToOneField(
        User,
        related_name="email_confirmation",
        verbose_name="email confirmation",
        on_delete=models.DO_NOTHING,
    )
    approval_code = models.CharField(
        max_length=128,
        verbose_name='Approve code',
        unique=True,
    )
    code_expiration_date = models.DateTimeField(
        verbose_name='code expiration date')
    is_approved = models.BooleanField(verbose_name='Approved?', default=False)


class BasicUser(User):
    objects = OnlyBasicUserManager()

    class Meta:
        proxy = True


class Mediator(User):
    objects = MediatorManager()

    class Meta:
        ordering = ['create_at']
        proxy = True


class AdditionalInfo(Mediator):
    mediator = models.OneToOneField(
        Mediator,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='get_info',
    )
    rate = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
