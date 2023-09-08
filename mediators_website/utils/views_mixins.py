from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.forms import Form
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
        return redirect(settings.SUCCESS_LOGIN_URL)


class FormValidMessageMixin:
    """
         Added success message to request (for example: "Successful authorization")
    """
    success_message = ""

    def form_valid(self, form, *args, **kwargs):
        response = super().form_valid(form, *args, **kwargs)
        success_message = self.get_success_message(form)
        messages.success(self.request, success_message)
        return response

    def get_success_message(self, form: Form):
        return self.success_message


class NextPageMixin:
    @property
    def success_url(self):
        return self.request.GET.get('next') or self.request.path
