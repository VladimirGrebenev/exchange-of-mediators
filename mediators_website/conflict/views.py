from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import request
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render, redirect

from django.contrib import messages
from django.urls import reverse_lazy, reverse

import logging

from django.views import View
from django.views.generic import FormView, TemplateView, CreateView, DetailView

from conflict.forms import ConflictForm, DocumentForm, RespondentsForm
from conflict.models import Conflict, Document, ConflictMessage
from user.models import BasicUser

LEVEL_MESSAGE = 50


class ConflictView(TemplateView):
    """
        Temporary view. Retire in the future
    """
    template_name = 'dashboard/page-dashboard-create-project.html'
    extra_context = {
        "object_list": Conflict.objects.all().prefetch_related('files')
    }


class ConflictFormView(FormView):
    """
        Returned conflict form
    """
    template_name = "dashboard/page-dashboard-create-project.html"
    form_class = ConflictForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if pk := self.request.GET.get('pk'):
            try:
                conflict = Conflict.objects.get(pk=pk)
                kwargs['instance'] = conflict
            except Conflict.DoesNotExist:
                pass
        return kwargs | {"user": self.request.user}


# class DocumentFormView(FormView):
# """
#     Returned document form
# """
# template_name = "conflict/document_form.html"
# form_class = DocumentForm
#
# def get_form_kwargs(self):
#     kwargs = super().get_form_kwargs()
#     if pk := self.request.GET.get('pk'):
#         try:
#             document = Document.objects.get(pk=pk)
#             kwargs['instance'] = document
#         except Document.DoesNotExist:
#             pass
#     return kwargs | {"user": self.request.user}

class DocumentFormView(FormView):
    """
        Returned document form
    """
    template_name = "conflict/document_form.html"
    form_class = DocumentForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if pk := self.request.GET.get('pk'):
            try:
                document = Document.objects.get(pk=pk)
                kwargs['instance'] = document
            except Document.DoesNotExist:
                pass
        return kwargs | {"user": self.request.user}


# Настройка логгера
logger = logging.getLogger(__name__)


class ConflictCreateView(CreateView):
    model = Conflict
    form_class = ConflictForm
    success_url = "/dashboard/create-project/"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        logger.info("Я попал в form_valid ")
        # Сохраняем форму конфликта

        conflict = form.save(commit=True)
        messages.success(
            self.request,
            f'Вы участник {form.cleaned_data["title"]}',
        )

        # Логируем данные формы
        logger.info("Данные формы успешно прошли проверку")
        return redirect(reverse('dashboard:user-conflict-review', kwargs={'pk': conflict.id}))

    def form_invalid(self, form):
        context = {'form': form}
        messages.error(self.request, 'Ошибка заполнения формы', extra_tags='danger')
        return render(self.request, self.template_name, context)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        form = ConflictForm(initial={'creator': self.request.user})
        context['form'] = form
        return context


class UserConflictWorkplacelView(LoginRequiredMixin, DetailView):
    """Получение рабочей страницы конфликта у юзера"""
    model = Conflict
    template_name = 'dashboard/page-dashboard-user-conflict-workplace.html'
    context_object_name = 'conflict'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = kwargs['object'].pk
        context['room_name'] = kwargs['object'].pk
        conflict_messages = ConflictMessage.objects.filter(conflict_id=room)
        context['conflict_messages'] = conflict_messages
        context['form'] = RespondentsForm()
        return context

    def post(self, request, *args, **kwargs):
        """Добавление участников конфликта"""
        form = RespondentsForm(request.POST)
        if form.is_valid():
            conflict = self.get_object()
            respondents = form.cleaned_data.get('respondents', [])
            for respondent in respondents:
                conflict.respondents.add(respondent)
            return redirect('dashboard:conflict-workplace', pk=conflict.pk)
        return render(request, 'dashboard/page-dashboard-conflict-workplace.html')


class MediatorConflictWorkplacelView(LoginRequiredMixin, DetailView):
    """Получение рабочей страницы конфликта у медиатора"""
    model = Conflict
    template_name = 'dashboard/page-dashboard-conflict-workplace.html'
    context_object_name = 'conflict'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RespondentsForm()

        room = kwargs['object'].pk
        context['room_name'] = kwargs['object'].pk
        conflict_messages = ConflictMessage.objects.filter(conflict_id=room)
        context['conflict_messages'] = conflict_messages
        return context

    def post(self, request, *args, **kwargs):
        form = RespondentsForm(request.POST)
        if 'status' in request.POST:
            """Завершение конфликта"""
            status = request.POST["status"]
            conflict = self.get_object()
            conflict.status = status
            conflict.save()
            return redirect('dashboard:conflict-workplace', pk=conflict.pk)
        if form.is_valid():
            """Добавление участников конфликта"""
            conflict = self.get_object()
            respondents = form.cleaned_data.get('respondents', [])
            for respondent in respondents:
                conflict.respondents.add(respondent)
            return redirect('dashboard:conflict-workplace', pk=conflict.pk)
        return render(request, 'dashboard/page-dashboard-conflict-workplace.html')

