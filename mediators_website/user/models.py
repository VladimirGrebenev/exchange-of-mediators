from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from .mediators_website.conflict.models import Conflict


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


class Document_types(models.Model):
    """Модель типов файлов"""
    id = models.BigAutoField(primary_key=True, unique=True)
    title = models.CharField(max_length=150, null=False, blank=False, unique=True)

    def __str__(self):
        return self.title


class Documents(models.Model):
    """Модель документов"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    type_id = models.ForeignKey(Document_types, on_delete=models.SET_NULL, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    file_path = models.FileField(upload_to='documents_users', null=True)
    is_all_visible = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id}'


# class Conflicts(models.Model):
#     pass


class Documents_conflicts(models.Model):
    """Модель привязки документа к конфликту"""
    document_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True)
    conflict_id = models.ForeignKey(Conflict, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.document_id, self.conflict_id
