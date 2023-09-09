from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .forms import UserForm, DocumentsForm
from .models import Document, EmailConfirmation

User = get_user_model()


class Document_typeListView(ListView):
    """Список типов файлов"""
    model = Document
    template_name = 'documents_list.html'
    context_object_name = 'documents_list'


class DocumentsCreateView(CreateView):
    """Добавление документа в БД"""
    model = Document
    form_class = DocumentsForm
    template_name = 'document_create.html'
    success_url = reverse_lazy('create_document')


class DocumentsListView(ListView):
    """Список документов"""
    model = Document
    template_name = 'documents_list.html'
    context_object_name = 'documents_list'


class DocumentsUpdateView(UpdateView):
    """Обновление документа"""
    model = Document
    form_class = DocumentsForm
    template_name = 'documents_update.html'
    success_url = reverse_lazy('documents_list')


class DocumentsDeleteView(DeleteView):
    """Удаление документов"""
    model = Document
    template_name = 'documents_list.html'
    success_url = reverse_lazy('documents_list')


class UserListView(ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'


class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('user_list')


class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('user_list')


class UserDeleteView(DeleteView):
    model = User
    template_name = 'user_confirm_delete.html'
    success_url = reverse_lazy('user_list')


class EmailConfirmView(View):
    def get(self, request, code):
        try:
            email = EmailConfirmation.objects.get(approval_code=code)
        except EmailConfirmation.DoesNotExist:
            messages.error(request, 'Something went wrong, try again and contact with technicals')
        else:
            email.is_approved = True
            email.save()
            messages.success(request, 'Mail has been successfully confirmed')
        return redirect(settings.LOGIN_URL)
