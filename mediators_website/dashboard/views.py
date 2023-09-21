from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from django.db.models import Q

from utils.views_mixins import PermissionByGroupMixin

from conflict.models import Conflict


class DashboardDispatcherView(LoginRequiredMixin, View):
    """
        Dashboard dispatcher by groups.
    """

    def dispatch(self, request, *args, **kwargs):
        if "mediator" in self.request.user.permission_groups:
            return HttpResponseRedirect(reverse('dashboard:mediator_dashboard'))
        return HttpResponseRedirect(reverse('dashboard:user_dashboard'))

    def handle_no_permission(self):
        return redirect(reverse('index'))


class UserDashboardView(LoginRequiredMixin, PermissionByGroupMixin, TemplateView):
    """
        User dashboard
    """
    allowed_groups = ('user',)
    template_name = 'page-dashboard.html'


class MediatorsDashboardView(LoginRequiredMixin, PermissionByGroupMixin, TemplateView):
    """
        Mediators dashboard
    """
    allowed_groups = ('mediator',)
    template_name = 'dashboard/page-dashboard.html'


class UserDashboardListConflictsView(LoginRequiredMixin,
                                     PermissionByGroupMixin, TemplateView):
    """
        User dashboard / conflicts list
    """
    allowed_groups = ('user',)
    template_name = 'dashboard/page-dashboard-manage-job.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Filter conflicts created by the user and not deleted
        conflicts = Conflict.objects.filter(
            Q(creator=user) | Q(respondents=user), deleted=False)
        context['conflicts'] = conflicts
        return context


class MediatorDashboardListConflictsView(LoginRequiredMixin,
                                     PermissionByGroupMixin, TemplateView):
    """
        Mediators dashboard / conflicts list
    """
    allowed_groups = ('mediator',)
    template_name = 'dashboard/page-dashboard-manage-job-mediator.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Filter conflicts created by the user and not deleted
        conflicts = Conflict.objects.filter(mediator=user, deleted=False)
        context['conflicts'] = conflicts
        return context