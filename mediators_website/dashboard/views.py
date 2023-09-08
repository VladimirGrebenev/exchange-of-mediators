from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View

from utils.views_mixins import PermissionByGroupMixin


class DashboardDispatcherView(View):

    def dispatch(self, request, *args, **kwargs):
        if "mediator" in self.request.user.groups.all():
            return HttpResponseRedirect(reverse('dashboard:mediator_dashboard'))
        return HttpResponseRedirect(reverse('dashboard:user_dashboard'))


class UserDashboardView(PermissionByGroupMixin, View):
    allowed_groups = ('user')
    pass


class MediatorsDashboardView(PermissionByGroupMixin, View):
    allowed_groups = ('mediator')
    pass
