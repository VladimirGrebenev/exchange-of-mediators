from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from user.models import User, Mediator, BasicUser


class Review(models.Model):
    to_user = models.ForeignKey(
        Mediator,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_("От кого")
    )
    from_user = models.ForeignKey(
        BasicUser,
        on_delete=models.CASCADE,
        related_name='created_reviews',
        verbose_name=_("Кому")
    )
    rating = models.IntegerField(
        verbose_name=_("Рейтинг"),
        error_messages={
            'required': 'Оцените медиатора',
            'invalid': 'Пожалуйста, оцените медиатора',
        },
    )
    text = models.TextField(verbose_name=_("Текст"))
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Создан")
    )

    class Meta:
        verbose_name = _('Отзыв')
        verbose_name_plural = _("Отзывы")
        ordering = ['-created_at']
