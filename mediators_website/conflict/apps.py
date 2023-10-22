from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ConflictConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'conflict'
    verbose_name = _("Поданные обращения")
