from django.contrib.auth.models import Group
from django.db import models


class MediatorManager(models.Manager):
    def get_queryset(self):
        mediator_group, _ = Group.objects.get_or_create(name='mediator')
        return super().get_queryset().filter(groups__in=[mediator_group])


class OnlyBasicUserManager(models.Manager):
    def get_queryset(self):
        user_group, _ = Group.objects.get_or_create(name='user')
        return super().get_queryset().filter(groups__in=[user_group])
