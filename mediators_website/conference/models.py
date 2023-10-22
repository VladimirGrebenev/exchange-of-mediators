from uuid import uuid4

from django.db import models
# from conflicts.models import Conflicts # For future
from django.utils.translation import gettext_lazy as _

from conflict.models import Conflict
from user.models import User


class Conferences(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True,
                          verbose_name=_("ID конференции"))
    conflict_id = models.ForeignKey(Conflict, on_delete=models.CASCADE, verbose_name=_("ID обращения"))
    initiator = models.ForeignKey(User, related_name='initiator',
                                  on_delete=models.CASCADE,
                                  verbose_name=_("Инициатор"))
    invated_user = models.ManyToManyField(User, verbose_name=_("Приглашенные"))
    created_at = models.DateTimeField(auto_now=True, editable=False,
                                      verbose_name=_("Создана"))
    scheduled_date = models.DateTimeField(verbose_name=_("Планируемая дата"))

    # file_path = models.FilePathField(path='conflicts_doc/', blank=True,
    #                                  null=True, verbose_name=_("Документы"))

    class Meta:
        verbose_name = _("Конференция")
        verbose_name_plural = _("Конференции")
        ordering = ['created_at']
