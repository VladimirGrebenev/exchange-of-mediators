from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

USERS = [(1, _("Иванов")),
         (2, _("Петров")),
         (3, _("Сидоров")),
         ]  # Заглушка


def user_directory_path(instance, filename):
    """ returns the path to the uploaded file """
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    # сюда желательно добавить ID конфликта между 0 и 1.
    return "user_{0}/{1}".format(instance.user.id, filename)


class DocumentType(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title


class Conflict(models.Model):
    """ class for creating a request """

    class Status(models.TextChoices):
        ACTIVE = 'active'
        CLOSED = 'closed'

    id = models.UUIDField(primary_key=True, default=uuid4)
    title = models.CharField(max_length=256, verbose_name="Title")
    status = models.TextField(choices=Status.choices, default=Status.ACTIVE)
    # creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
    #                             verbose_name=_("Applicant"))
    # respondent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
    #                                related_name='defendant')
    creator = models.CharField(max_length=250, choices=USERS,
                               default='by appointment')
    respondent = models.CharField(max_length=250, choices=USERS,
                                  default='by appointment')
    description = models.TextField(blank=True, null=True,
                                   verbose_name="Description")
    description_as_visible = models.BooleanField(default=False,
                                                 verbose_name="As visible")

    concluded_contract = models.BooleanField(default=False,
                                             verbose_name="Signed contract")
    personal_data_processed = models.BooleanField(default=False,
                                                  verbose_name="Permission to process data")
    respect_confidentiality = models.BooleanField(default=False,
                                                  verbose_name="Respect confidentiality")
    mediator = models.CharField(max_length=250, choices=USERS,
                                default='by appointment')
    body_as_markdown = models.BooleanField(default=False,
                                           verbose_name="As markdown")
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
        verbose_name = _("Appeal")
        verbose_name_plural = _("Appeal")
        ordering = ("-created",)


class Document(models.Model):  # document
    """ class for uploading documents """
    id = models.UUIDField(primary_key=True, default=uuid4)
    # user = models.ForeignKey(User, on_delete=models.CASCADE,
    #                          related_name='documents')
    user = models.CharField(max_length=250, choices=USERS,
                            default='by appointment')
    conflict = models.ForeignKey(Conflict, on_delete=models.CASCADE,
                                 related_name='files')
    type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,
                                   editable=False)
    updated = models.DateTimeField(auto_now=True,
                                   editable=False)
    file_as_visible = models.BooleanField(default=False,
                                          verbose_name="As visible")
    file_path = models.FileField(upload_to=user_directory_path)
