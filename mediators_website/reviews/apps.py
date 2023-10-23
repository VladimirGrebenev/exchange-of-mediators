from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UserReviewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reviews'
    verbose_name = _("Отзывы")
