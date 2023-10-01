from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from django.views.generic import TemplateView, CreateView, ListView
from django.db.models import Q
from user.models import Mediator

from utils.views_mixins import PermissionByGroupMixin

from conflict.models import Conflict
# from conflict.forms import ConflictForm
# from conflict.views import ConflictCreateView

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


class UserDashboardView(LoginRequiredMixin, PermissionByGroupMixin, ListView):
    """
        User dashboard
    """
    allowed_groups = ('user',)
    template_name = 'page-dashboard.html'

    model = Mediator

    def get_context_data(self, **kwargs):
        """
        Отображение полного списка медиаторов внизу страницы
        """
        context = super().get_context_data(**kwargs)

        mediators = Mediator.objects.all().order_by('create_at')
        num_mediators = min(mediators.count(), 3)  # если медиаторов меньше трех, берем число медиаторов, иначе 3
        context['objects_mediators'] = mediators[:num_mediators]
        if num_mediators > 1:
            context['last_mediator'] = mediators[
                num_mediators - 1]  # Нужно чтобы не ставить в шаблоне черту после последнего элемента
        else:
            context['last_mediator'] = 0
        return context


class MediatorsDashboardView(LoginRequiredMixin, PermissionByGroupMixin, ListView):
    """
        Mediators dashboard
    """
    allowed_groups = ('mediator',)
    template_name = 'dashboard/page-dashboard.html'

    model = Mediator

    def get_context_data(self, **kwargs):
        """
        Отображение полного списка медиаторов внизу страницы
        """
        context = super().get_context_data(**kwargs)

        mediators = Mediator.objects.all().order_by('create_at')
        num_mediators = min(mediators.count(), 3) # если медиаторов меньше трех, берем число медиаторов, иначе 3
        context['objects_mediators'] = mediators[:num_mediators]
        if num_mediators > 1:
            context['last_mediator'] = mediators[num_mediators-1] # Нужно чтобы не ставить в шаблоне черту после последнего элемента
        else:
            context['last_mediator'] = 0
        return context


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
