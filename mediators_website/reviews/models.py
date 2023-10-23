from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from user.models import User, Mediator


class Review(models.Model):
    to_user = models.ForeignKey(Mediator, on_delete=models.CASCADE,
                                related_name='reviews',
                                verbose_name=_("От кого"))
    from_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                  verbose_name=_("Кому"))
    rating = models.IntegerField(blank=False, null=False,
                                 verbose_name=_("Рейтинг"))
    text = models.TextField(null=True, blank=True, verbose_name=_("Текст"))
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_("Создан"))

    # def get_absolute_url(self):
    #     return reverse('review-detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = _('Отзыв')
        verbose_name_plural = _("Отзывы")
        ordering = ['-created_at']
