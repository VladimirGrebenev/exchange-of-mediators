from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.auth.models import Group
from django.shortcuts import render


class NotFoundMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            return render(request, 'page-error.html')
        return response


class AttachUserGroupsMiddleware(AuthenticationMiddleware):
    """
        Added permission groups and groups permissions to request user
    """
    def process_request(self, request):
        user = request.user

        if user.is_authenticated:
            groups = user.groups.values_list('name', flat=True)
            if not groups:
                user_group, _ = Group.objects.get_or_create(name="user")
                user.groups.set([user_group])
                setattr(user, "permission_groups", [user_group.name])
            else:
                setattr(user, "permission_groups", groups)
            setattr(user, "permissions", user.get_all_permissions())
        else:
            setattr(user, "permissions", set())
        super().process_request(request)
