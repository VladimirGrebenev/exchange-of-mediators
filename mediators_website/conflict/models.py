import uuid
from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

from user.models import User, NULLABLE, Mediator
from utils.common import pluralize_word


def user_directory_path(instance, filename):
    """ returns the path to the uploaded file """
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    # сюда желательно добавить ID конфликта между 0 и 1.
    return "user_{0}/{1}".format(instance.user.id, filename)


class StatusChoices(models.TextChoices):
    """ Conflict Status Selection Class """
    IN_PROCESS = 'В работе', _('В работе')
    CLOSED = 'Завершен', _('Завершен')
    NEW = 'Новый', _('Новый')
    # DRAFT = 'Черновик', _('Черновик')


class MediatorsLevel(models.TextChoices):
    """ Mediator Level Selection Class"""
    CHOOSE = 'не выбрано', _('не выбрано')
    BIGINNER_LEVEL = 'новичок', _('новичок')
    EXPERIENCED = 'бывалый', _('бывалый')
    EXPENSIVE = 'дорогой', _('дорогой')
    GOD_LEVEL = 'уровень Бог', _('уровень Бог')


class ConflictCategory(models.TextChoices):
    """ Conflict Category Selection Class """
    CHOOSE = 'не выбрано', _('не выбрано')
    CORPORATE = 'корпоративный', _('корпоративный')
    BUSINESS = 'бизнес', _('бизнес')
    FAMILY = 'семейный', _('семейный')
    REAL_ESTATE = 'недвижимость', _('недвижимость')
    HERITAGE = 'наследство', _('наследство')
    PERSONAL = 'личный', _('личный')


class PriseChoices(models.TextChoices):
    """ Price Selection Class """
    CHOOSE = 'не выбрано', _('не выбрано')
    LOW = 'низкая', _('низкая')
    MEDIUM = 'средняя', _('средняя')
    HIGH = 'высокая', _('высокая')


class LanguageLevel(models.TextChoices):
    """ Language Level Class """
    BASIC_A_1 = 'A1', _(' A1 — Уровень выживания (Survival Level: Beginner и Elementary)')
    BASIC_A_2 = 'A2', _(' A2 — Предпороговый уровень (Waystage: Pre-Intermediate)')
    INDEPENDENT_B_1 = 'B1', _(' B1 — Пороговый уровень (Threshold: Intermediate)')
    INDEPENDENT_B_2 = 'B2', _(' B2 — Пороговый продвинутый уровень (Vantage: Upper-Intermediate)')
    PROFICIENT_C_1 = 'C1', _(' C1 — Уровень профессионального владения (Effective Operational Proficiency: Advanced)')
    PROFICIENT_C_2 = 'C2', _(' C2 — Уровень владения в совершенстве (Mastery: Proficiency)')


class DecidedTime(models.TextChoices):
    """ Time Selection Class """
    CHOOSE = 'не выбрано', _('не выбрано')
    ONE_DAY = '1 День', _('1 День')
    TWO_DAYS = '2 Дня', _('2 Дня')
    THREE_DAYS = '3 Дня', _('3 Дня')
    WEEK = '1 Неделя', _('1 Неделя')


class Conflict(models.Model):
    """ class for creating a request """

    status = models.TextField(choices=StatusChoices.choices, null=True,
                              default=StatusChoices.NEW,
                              verbose_name=_("Статус"))
    category = models.TextField(choices=ConflictCategory.choices,
                                default=ConflictCategory.CHOOSE,
                                verbose_name=_("Категория"))
    # mediators_level = models.TextField(choices=MediatorsLevel.choices,
    #                                    default=MediatorsLevel.CHOOSE,
    #                                    verbose_name=_("Уровень медиатора"))
    # prise = models.TextField(choices=PriseChoices.choices,
    #                          default=PriseChoices.CHOOSE,
    #                          verbose_name=_("Цена"))
    fixed_price = models.CharField(max_length=256, null=True, verbose_name=_("Цена"))
    decide_time = models.TextField(choices=DecidedTime.choices,
                                   default=DecidedTime.CHOOSE,
                                   verbose_name=_("Время на решение"))
    country = models.CharField(max_length=256, null=True, verbose_name=_("Страна"))
    city = models.CharField(max_length=256, null=True, verbose_name=_("Город"))
    # language = models.CharField(max_length=256, null=True, verbose_name=_("Язык"))
    # language_level = models.TextField(choices=LanguageLevel.choices,
    #                                   default=LanguageLevel.BASIC_A_1,
    #                                   verbose_name=_("Уровень владения языком"))
    id = models.UUIDField(primary_key=True, default=uuid4)
    title = models.CharField(max_length=256, verbose_name=_("Заголовок обращения"))
    creator = models.ForeignKey(User, on_delete=models.CASCADE,
                                verbose_name=_("Заявитель"), related_name='created_conflicts')
    mediator = models.ForeignKey(User, on_delete=models.CASCADE,
                                 verbose_name=_("Медиатор"), **NULLABLE,
                                 related_name='ownable_conflicts')
    respondents = models.ManyToManyField(
        User,
        related_name='conflicts_as_respondent',
        verbose_name=_('Остальные участники'),
        **NULLABLE,
    )
    description = models.TextField(blank=True, null=True,
                                   verbose_name=_("Описание"))
    # is_all_visible = models.BooleanField(
    #     default=False,
    #     verbose_name=_("Доступно для всех?")
    # )
    created = models.DateTimeField(auto_now_add=True,
                                   editable=False)
    updated = models.DateTimeField(auto_now=True,
                                   editable=False)
    deleted = models.BooleanField(default=False, editable=False)
    closed_at = models.DateTimeField(auto_now=True,
                                     editable=False)

    def __str__(self) -> str:
        return f"{self.pk} {self.title}"

    def delete(self, *args):
        self.deleted = True
        self.save()

    class Meta:
        verbose_name = _("Conflict")
        verbose_name_plural = _("Conflict")
        ordering = ("-created",)


class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name='files', on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    conflict = models.ForeignKey(
        Conflict,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name=_('Обращение'),
        **NULLABLE,
    )
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    file_path = models.FileField(upload_to='documents_users', null=True)
    is_all_visible = models.BooleanField(default=False, verbose_name='Виден всем?')

    def __str__(self):
        return f'{self.id}'


class ConflictResponse(models.Model):
    """
    Модель для откликов на конфликты
    """
    id = models.UUIDField(primary_key=True, default=uuid4)
    conflict = models.ForeignKey(Conflict,
                                 on_delete=models.CASCADE,
                                 related_name='responses',
                                 )
    mediator = models.ForeignKey(Mediator,
                                 on_delete=models.CASCADE,
                                 related_name='conflicts',
                                 )
    response_time = models.DateTimeField(auto_now_add=True,
                                         editable=False)
    rate = models.IntegerField(blank=False, null=False)  # Ставка от медиатора
    comment = models.TextField(blank=True, null=True)  # Комментарий от медиатора
    time_for_conflict = models.IntegerField(blank=True, null=True)  # Время на решение конфликта

    class Meta:
        ordering = ['-response_time']

    def time_on_resolved(self) -> str:
        if self.time_for_conflict is None:
            return ''

        return (f"{self.time_for_conflict} "
                f"{pluralize_word(self.time_for_conflict, 'день', 'дня', 'дней')}")

    def count_reviews(self) -> str:
        return (f"{self.mediator.reviews.count()} "
                f"{pluralize_word(self.mediator.reviews.count(), 'отзыв', 'отзыва', 'отзывов')}")
