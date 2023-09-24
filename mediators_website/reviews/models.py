from django.db import models
from user.models import User


class Review(models.Model):
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(blank=False, null=False)
    text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
