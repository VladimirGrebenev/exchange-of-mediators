from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
import uuid

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
        return f'{self.firstname} {self.lastname}, {self.email}'


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


class AdditionalInfo(Mediator):
    mediator = models.OneToOneField(
        Mediator,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='add_info_for_mediator',
    )
    rate = models.IntegerField(blank=True, null=True)
    photo = models.FilePathField(path='mediators_photo/', blank=True, null=True)
    summary = models.IntegerField(blank=True, null=True)

class MediatorType(models.TextChoices):
    TYPE_A = "Type A"
    TYPE_B = "Type B"
    TYPE_C = "Type C"
    TYPE_D = "Type D"

class AdditionalInfo(models.Model):
    user = models.OneToOneField(
        Mediator,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    description = models.TextField()
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    successful_cases_procentage = models.DecimalField(
        max_digits=5, decimal_places=2
    )
    type = models.CharField(
        max_length=50,
        choices=MediatorType.choices,
    )

    def __str__(self):
        return self.mediator.email
