from random import sample

from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.views.generic.base import ContextMixin
from django.db.models import Count

from user.models import Mediator


class PermissionByGroupMixin(UserPassesTestMixin):
    is_superuser_only: bool = False
    allowed_groups: list = []

    def test_func(self) -> bool:
        user = self.request.user
        if self.is_superuser_only:
            return user.is_superuser
        result = any(
            group in user.permission_groups for group in self.allowed_groups
        )
        return result or user.is_superuser

    def handle_no_permission(self):
        return redirect(settings.LOGIN_REDIRECT_URL)


class NextPageMixin:
    """
        Redirect mixin. U can use it with query_para next like:
        '{% url 'create_profile' pk=pk %}?next={% url 'dashboard:dashboard' %}'
    """

    @property
    def success_url(self):
        return self.request.GET.get('next') or self.request.path


class TopFiveMediatorsMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mediators = Mediator.objects.all().order_by('lastname')
        num_mediators = min(mediators.count(), 5)  # определяем количество записей или возьмем 5
        random_mediators_list = sample(list(mediators), num_mediators)  # выбираем случайные записи из модели
        context['top_mediators'] = random_mediators_list
        return context


