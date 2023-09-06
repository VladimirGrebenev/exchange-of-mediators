from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class Statuses(models.TextChoices):
    NEW = "New"
    APPROVED = "Approved"
    BLOCKED = "Blocked"
    DECLINED = "Declined"


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstname = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150)
    email = models.CharField(max_length=150, required=True, unique=True)
    phone = models.CharField(max_length=12, unique=True)
    birthday = models.DateField()
    create_at = models.DateTimeField(auto_now_add=True)
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
