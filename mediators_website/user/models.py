from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


NULLABLE = {'blank': True, 'null': True}


class Statuses(models.TextChoices):
    NEW = "New"
    APPROVED = "Approved"
    BLOCKED = "Blocked"
    DECLINED = "Declined"


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstname = models.CharField(max_length=150, **NULLABLE)
    lastname = models.CharField(max_length=150, **NULLABLE)
    email = models.CharField(max_length=150, null=False, blank=False, unique=True)
    phone = models.CharField(max_length=12, **NULLABLE)
    birthday = models.DateField(**NULLABLE)
    create_at = models.DateTimeField(auto_now_add=True, **NULLABLE)
    is_superuser = models.BooleanField(default=False)
    status = models.TextField(
        verbose_name="status",
        choices=Statuses.choices,
        default=Statuses.NEW,
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.email
