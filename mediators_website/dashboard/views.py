from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.http import HttpResponseServerError
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q
from django.contrib import messages

from user.models import Mediator, BasicUser, User, UserMessage, ContactUser

from utils.views_mixins import PermissionByGroupMixin
from utils.common import sample_queryset

from conflict.models import Conflict
from conflict.forms import ResponseForm, ResponseUserForm
from user.forms import ContactForm

import logging

# from conflict.forms import ConflictForm
# from conflict.views import ConflictCreateView


class DashboardDispatcherView(LoginRequiredMixin, View):
    """
        Dashboard dispatcher by groups.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if "mediator" in self.request.user.permission_groups:
            return HttpResponseRedirect(
                reverse('dashboard:mediator_dashboard'))
        return HttpResponseRedirect(reverse('dashboard:user_dashboard'))

    def handle_no_permission(self):
        return redirect(reverse('signing:login'))


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
                                     PermissionByGroupMixin, ListView):
    """
        User dashboard / conflicts list
    """
    allowed_groups = ('user',)
    model = Conflict
    template_name = 'dashboard/page-dashboard-manage-jobs.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = self.request.user
#         # Filter conflicts created by the user and not deleted
#         conflicts = Conflict.objects.filter(
#             Q(creator=user) | Q(respondents=user), deleted=False)
#         # context['conflicts'] = conflicts
#         # return context
#         # Создаем пагинатор только для conflicts
#         paginator = Paginator(conflicts, self.paginate_by)
#         page = self.request.GET.get(
#             'page')  # Получаем текущий номер страницы из запроса
#         conflicts_page = paginator.get_page(
#             page)  # Получаем конфликты для текущей страницы
#         context['conflicts'] = conflicts_page
#         return context

    context_object_name = 'conflicts'
    paginate_by = 10 # Количество конфликтов на одной странице

    def get_queryset(self):
        return Conflict.objects.filter(Q(creator=self.request.user) | Q(respondents=self.request.user)).distinct()
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user = self.request.user
    #     # Filter conflicts created by the user and not deleted
    #     conflicts = Conflict.objects.filter(
    #         Q(creator=user) | Q(respondents=user), deleted=False)
    #     context['conflicts'] = conflicts
    #     return context


class MediatorDashboardListConflictsView(LoginRequiredMixin,
                                         PermissionByGroupMixin, ListView):
    """
        Mediators dashboard / conflicts list
    """
    allowed_groups = ('mediator',)
    template_name = 'dashboard/page-dashboard-manage-job-mediator.html'
    model = Conflict
    context_object_name = 'conflicts'
    paginate_by = 5

    def get_queryset(self):
        work_conflicts = Conflict.objects.filter(mediator=self.request.user, deleted=False)
        new_conflicts = Conflict.objects.filter(responses__mediator=self.request.user)
        conflicts = list(set(new_conflicts) | set(work_conflicts))
        print(Conflict.objects.filter(mediator=self.request.user).count())
        return conflicts



class MediatorsDashboardNewConflictsListView(LoginRequiredMixin,
                                         PermissionByGroupMixin, View):
    """
    Список новых конфликтов для медиатора
    """
    allowed_groups = ('mediator',)
    template_name = 'dashboard/page-dashboard-new-conflicts-list.html'
    model = Mediator
    context_object_name = 'conflicts'
    paginate_by = 10  # Количество конфликтов на одной странице

    def get(self, request, *args, **kwargs):
        mediator = self.request.user
        category = request.GET.get('category',
                                   'all')  # Получаем значение категории из запроса


        new_conflicts = Conflict.objects.filter(status="Новый",
                                                    deleted=False)


        # Создаем пагинатор только для new_conflicts
        paginator = Paginator(new_conflicts, self.paginate_by)
        page = request.GET.get(
            'page')  # Получаем текущий номер страницы из запроса
        conflicts_page = paginator.get_page(
            page)  # Получаем конфликты для текущей страницы

        context = {
            'mediator': mediator,
            'new_conflicts': conflicts_page,
            'all_conflicts': new_conflicts,
            'selected_categories': category,
        }
        return render(request, self.template_name, context)

def filter_conflicts(request):
    try:
        categories = request.GET.get('categories').split(",")
        sorting = request.GET.get('sorting')
        print(sorting)

        if 'all' in categories:
            conflicts = Conflict.objects.filter(status="Новый",
                                                deleted=False)
        else:
            conflicts = Conflict.objects.filter(category__in=categories,
                                                status="Новый",
                                                        deleted=False)

        if sorting == 'Сначала новые':
            conflicts = conflicts.order_by('-created')
        elif sorting == 'Сначала старые':
            conflicts = conflicts.order_by('created')
        elif sorting == 'Сначала недорогие':
            conflicts = conflicts.order_by('fixed_price')
        else:
            conflicts = conflicts.order_by('-fixed_price')

        context = {'conflicts': conflicts}
        return render(request, 'dashboard/conflict_list.html', context)
    except Exception as e:
        logging.error(str(e))
        # Handle the exception or return an appropriate response
        return HttpResponseServerError("An error occurred while filtering conflicts.")


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
                'rate': conflict.fixed_price,
            }
        )
        context['form'] = form
        return context

    def get_success_url(self):
        # Возвращаем URL текущей страницы
        return self.request.path

    def post(self, request, *args, **kwargs):
        form = ResponseForm(request.POST)
        conflict = Conflict.objects.get(pk=kwargs.get('pk'))
        mediator = request.user

        if form.is_valid():
            # Если отклик был, скажем до свидания
            if conflict.responses.filter(mediator=mediator).count() > 0:
                messages.info(request, 'Вы уже оставляли отклик')
                return redirect(self.get_success_url())

            form.save()
            messages.success(self.request, f'Ваш отклик опубликован',)
            return redirect(self.get_success_url())

        messages.error(self.request, f'Ошибка заполнения формы', extra_tags='danger')
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
                messages.success(request, 'Медиатор назначен')
                return redirect(reverse('dashboard:user-conflict-workplace', kwargs={'pk': conflict.id}))

        conflict = Conflict.objects.get(pk=kwargs.get('pk'))
        mediator = request.user
        context = {
            'conflict': conflict,
            'mediator': mediator,
            'form': form
        }
        return render(request, 'dashboard/page-dashboard-user-conflict-review.html', context)


class UserMessageView(LoginRequiredMixin, ListView):
    """Просмотр сообщений у User"""
    model = UserMessage
    template_name = 'dashboard/page-dashboard-my-messages.html'
    context_object_name = 'message'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        user_messages = UserMessage.objects.filter(Q(from_user=user.id) | Q(to_user=user.id))
        contacts_user = ContactUser.objects.filter(user=user.id)

        context['user_messages'] = user_messages
        context['user'] = user
        context['contacts_user'] = contacts_user
        context['form'] = ContactForm()
        return context

    def post(self, request, *args, **kwargs):
        """Добавление участников в контакты пользователя"""
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.cleaned_data.get('contact', [])
            try:
                ContactUser.objects.filter(user=self.request.user, contact=contact)[0]
            except IndexError:
                if self.request.user != contact:
                    contact_elem = ContactUser(user=self.request.user, contact=contact)
                    contact_elem.save()
            return redirect('dashboard:my-messages')
        return render(request, 'dashboard/page-dashboard-my-messages.html')


class UserMessageParamView(LoginRequiredMixin, ListView):
    """Просмотр сообщений у User при откртыии страницы с параметрами"""
    model = UserMessage
    template_name = 'dashboard/page-dashboard-my-messages.html'
    context_object_name = 'message'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user  # Пользователь основной
        id_user_from_pk = self.kwargs['u2']  # UUID пользователя из контактов
        user_from_pk = User.objects.filter(id=id_user_from_pk)[0]
        user_messages = UserMessage.objects.filter(
            Q(from_user=user.id, to_user=user_from_pk) | Q(from_user=user_from_pk, to_user=user.id))
        self.set_new_message_false(user=user, user_from_pk=user_from_pk)  # устанавливаем информацию о новых сообщениях в false

        contacts_user = ContactUser.objects.filter(user=user.id)
        context['user_messages'] = user_messages
        context['user'] = user
        context['contacts_user'] = contacts_user
        context['user_from_contact'] = user_from_pk
        context['id_user_from_pk'] = id_user_from_pk
        context['id_user'] = user.id
        context['form'] = ContactForm()
        return context

    def set_new_message_false(self, user, user_from_pk):
        """
        Функция для установки new_messages = False в контактах при открытии окна сообщений контакта
        """
        contact = ContactUser.objects.get(user=user.id, contact=user_from_pk)
        contact.new_messages = False
        contact.save()

    def post(self, request, *args, **kwargs):
        """Добавление участников в контакты пользователя"""
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.cleaned_data.get('contact', [])
            try:
                ContactUser.objects.filter(user=self.request.user, contact=contact)[0]
            except IndexError:
                if self.request.user != contact:
                    contact_elem = ContactUser(user=self.request.user, contact=contact)
                    contact_elem.save()

            return redirect('dashboard:my-messages')
        return render(request, 'dashboard/page-dashboard-my-messages.html')
