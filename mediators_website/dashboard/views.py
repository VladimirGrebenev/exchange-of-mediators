from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
# from conflict.forms import ConflictForm
# from conflict.views import ConflictCreateView
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView

# from utils.sample_objects import sample_queryset
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.db.models import Q

from user.models import Mediator, BasicUser

from utils.views_mixins import PermissionByGroupMixin
from utils.common import sample_queryset

from conflict.models import Conflict
from conflict.forms import ResponseForm, ResponseUserForm
# from conflict.forms import ConflictForm
# from conflict.views import ConflictCreateView


class DashboardDispatcherView(LoginRequiredMixin, View):
    """
        Dashboard dispatcher by groups.
    """

    def dispatch(self, request, *args, **kwargs):
        if "mediator" in self.request.user.permission_groups:
            return HttpResponseRedirect(
                reverse('dashboard:mediator_dashboard'))
        return HttpResponseRedirect(reverse('dashboard:user_dashboard'))

    def handle_no_permission(self):
        return redirect(reverse('index'))


class UserDashboardView(LoginRequiredMixin, PermissionByGroupMixin, ListView):
    """
        User dashboard
    """
    allowed_groups = ('user',)
    template_name = 'dashboard/page-dashboard-user.html'
    model = BasicUser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['conflicts'] = sample_queryset(Conflict, 3)
        return context


class MediatorsDashboardView(LoginRequiredMixin, PermissionByGroupMixin,
                             ListView):
    """
        Mediators dashboard
    """
    allowed_groups = ('mediator',)
    template_name = 'dashboard/page-dashboard-mediator.html'

    model = Mediator

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mediator = self.request.user
        conflicts = mediator.ownable_conflicts
        completed_conflicts = conflicts.filter(status='Завершен')
        active_conflicts = conflicts.exclude(status='Завершен')
        context['mediator'] = mediator
        context['completed_conflicts'] = completed_conflicts
        context['active_conflicts'] = active_conflicts
        return context


class UserDashboardListConflictsView(LoginRequiredMixin,
                                     PermissionByGroupMixin, TemplateView):
    """
        User dashboard / conflicts list
    """
    allowed_groups = ('user',)
    template_name = 'dashboard/page-dashboard-manage-jobs.html'

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


class UserDashboardListConflictStatusNew(UserDashboardListConflictsView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['conflicts'] = self.request.user.created_conflicts.filter(
            status='Новый').all()
        return context


class UserDashboardListConflictStatusInWork(UserDashboardListConflictsView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['conflicts'] = self.request.user.created_conflicts.filter(
            status='В работе').all()
        return context


class UserDashboardListConflictStatusCompleted(UserDashboardListConflictsView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['conflicts'] = self.request.user.created_conflicts.filter(
            status='Завершен').all()
        return context

      
class MediatorsDashboardNewConflictsView(LoginRequiredMixin,
                                         PermissionByGroupMixin, View):
    """
    Список новых конфликтов для медиатора
    """
    allowed_groups = ('mediator',)
    template_name = 'dashboard/page-dashboard-new-conflicts-list.html'
    model = Mediator
    context_object_name = 'conflicts'
    paginate_by = 10  # Количество конфликтов на одной странице

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        mediator = self.request.user
        category = request.GET.get('category',
                                   'all')  # Получаем значение категории из запроса

        if 'all' in category:
            new_conflicts = Conflict.objects.filter(status="Новый",
                                                    deleted=False)
        elif category:
            categories = category.split(',')
            new_conflicts = Conflict.objects.filter(status="Новый",
                                                    deleted=False,
                                                    category__in=categories)
        else:
            new_conflicts = Conflict.objects.filter(status="Новый",
                                                    deleted=False)

        # Создаем пагинатор только для new_conflicts
        paginator = Paginator(new_conflicts, self.paginate_by)
        page = request.GET.get(
            'page')  # Получаем текущий номер страницы из запроса
        conflicts_page = paginator.get_page(
            page)  # Получаем конфликты для текущей страницы

        # Если это AJAX-запрос
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            conflicts_list = [
                {
                    'category': conflict.category,
                    'title': conflict.title,
                    'description': conflict.description,
                    'fixed_price': conflict.fixed_price,
                    'city': conflict.city,
                    'country': conflict.country,
                    'created': conflict.created,
                    # поля, которые передаютсяь в AJAX ответе
                }
                for conflict in conflicts_page
            ]
            print(conflicts_list)
            return JsonResponse(conflicts_list, safe=False) # Однако, передается в ответ  HTML

        context = {
            'mediator': mediator,
            'new_conflicts': conflicts_page,
            'all_conflicts': new_conflicts,
            'selected_categories': category,
        }
        return render(request, self.template_name, context)

      
class MediatorConflictDetail(LoginRequiredMixin, PermissionByGroupMixin, DetailView):
    allowed_groups = ('mediator',)
    model = Conflict
    template_name = 'dashboard/page-dashboard-new-conflict-review.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conflict = context.get('conflict')
        form = ResponseForm(
            initial={
                'conflict': conflict.id,
                'mediator': self.request.user.id,
            }
        )
        context['form'] = form
        return context

    def get_success_url(self):
        # Возвращаем URL текущей страницы
        return self.request.path

    def post(self, request, *args, **kwargs):
        form = ResponseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.get_success_url())

        conflict = Conflict.objects.get(pk=kwargs.get('pk'))
        mediator = request.user
        context = {
            'conflict': conflict,
            'mediator': mediator,
            'form': form
        }
        return render(request, 'dashboard/page-dashboard-new-conflict-review.html', context)


class UserConflictDetail(LoginRequiredMixin, PermissionByGroupMixin, DetailView):
    allowed_groups = ('user',)
    model = Conflict
    template_name = 'dashboard/page-dashboard-user-conflict-review.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conflict = context.get('conflict')
        form = ResponseUserForm(
            initial={
                'conflict': conflict.id,
                'mediator': conflict.mediator,
            }
        )
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        form = ResponseUserForm(request.POST)
        try:
            request.POST["id"]
        except Exception:
            conflict_id = None
        else:
            conflict_id = request.POST["id"]
            conflict = Conflict.objects.get(pk=conflict_id)

            try:
                request.POST["status"]
            except Exception:
                status = None
            else:
                conflict.status = request.POST["status"]
                conflict.save()

            try:
                request.POST["mediat"]
            except Exception:
                mediat = None
            else:
                print(request.POST["mediat"])
                conflict.mediator = Mediator.objects.get(pk=request.POST["mediat"])
                conflict.status = 'В работе'
                conflict.save()

        conflict = Conflict.objects.get(pk=kwargs.get('pk'))
        mediator = request.user
        context = {
            'conflict': conflict,
            'mediator': mediator,
            'form': form
        }
        return render(request, 'dashboard/page-dashboard-user-conflict-review.html', context)
