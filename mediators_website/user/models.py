from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
import uuid

from conflict.models import Conflict
from user.object_managers import MediatorManager, OnlyBasicUserManager

NULLABLE = {'blank': True, 'null': True}


class Statuses(models.TextChoices):
    NEW = "New"
    APPROVED = "Approved"
    BLOCKED = "Blocked"
    DECLINED = "Declined"


class User(PermissionsMixin, AbstractBaseUser):
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

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class EmailConfirmation(models.Model):
    user = models.OneToOneField(
        User,
        related_name="email_confirmation",
        verbose_name="email confirmation",
        on_delete=models.DO_NOTHING,
    )
    approval_code = models.CharField(
        max_length=128,
        verbose_name='Approve code',
        unique=True,
    )
    code_expiration_date = models.DateTimeField(
        verbose_name='code expiration date')
    is_approved = models.BooleanField(verbose_name='Approved?', default=False)


class BasicUser(User):
    objects = OnlyBasicUserManager()

    class Meta:
        proxy = True


class Mediator(User):
    objects = MediatorManager()

    class Meta:
        proxy = True


class DocumentType(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True)
    title = models.CharField(max_length=150, null=False, blank=False, unique=True)

    def __str__(self):
        return self.title


class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(DocumentType, on_delete=models.SET_NULL, null=True)
    conflict = models.ForeignKey(Conflict, on_delete=models.CASCADE,
                                 related_name='files')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    file_path = models.FileField(upload_to='documents_users', null=True)
    is_all_visible = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id}'
