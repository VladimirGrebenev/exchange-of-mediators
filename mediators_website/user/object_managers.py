from django.db import models


class MediatorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(groups__name__in=["mediator"]).prefetch_related('groups')


class OnlyBasicUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(groups__name__in=["user"]).prefetch_related('groups')
