from django.http import request
from django.http import HttpRequest

from django.contrib import messages
from django.urls import reverse_lazy
import logging
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView, CreateView

from conflict.forms import ConflictForm, DocumentForm
from conflict.models import Conflict, Document

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
        print(form.cleaned_data)
        # Сохраняем форму конфликта

        conflict = form.save(commit=True)
        messages.add_message(
            self.request, LEVEL_MESSAGE, 
            f'Вы участник {form.cleaned_data["title"]}', 
            extra_tags='message_conflict',
            )

        # Логируем данные формы
        logger.info("Данные формы успешно прошли проверку")

        return super().form_valid(form)
        # Redirect to the success URL
        # return redirect(self.get_success_url())

    def get_form_kwargs(self):
        logger.info("get_form_kwargs ")
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Передаем текущего пользователя в форму
        return kwargs