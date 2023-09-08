from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


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
