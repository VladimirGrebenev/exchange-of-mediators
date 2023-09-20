import uuid
from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

from user.models import User, NULLABLE


def user_directory_path(instance, filename):
    """ returns the path to the uploaded file """
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    # сюда желательно добавить ID конфликта между 0 и 1.
    return "user_{0}/{1}".format(instance.user.id, filename)


class Status(models.TextChoices):
    IN_PROCESS = 'В работе'
    CLOSED = 'Завершен'
    NEW = 'Новый'
    DRAFT = 'Черновик'


class Conflict(models.Model):
    """ class for creating a request """

    id = models.UUIDField(primary_key=True, default=uuid4)
    title = models.CharField(max_length=256, verbose_name=_("Заголовок"))
    status = models.TextField(choices=Status.choices, default=Status.DRAFT)
    creator = models.ForeignKey(User, on_delete=models.CASCADE,
                                verbose_name=_("Заявитель"), related_name='created_conflicts')

    mediator = models.ForeignKey(User, on_delete=models.CASCADE,
                                 verbose_name=_("Медиатор"), **NULLABLE, related_name='ownable_conflicts')
    respondents = models.ManyToManyField(
        User,
        related_name='conflicts_as_respondent',
        verbose_name=_('Остальные участники'),
        # **NULLABLE,
    )
    description = models.TextField(blank=True, null=True,
                                   verbose_name=_("Описание"))
    is_all_visible = models.BooleanField(
        default=False,
        verbose_name=_("Доступно для всех?")
    )
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
