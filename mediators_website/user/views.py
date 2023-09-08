from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .forms import UserForm, DocumentsForm, Document_typesForm, Documents_conflictsForm
from .models import Documents, Document_types, Documents_conflicts

User = get_user_model()


class Documents_conflictsCreateView(CreateView):
    """Привязка документа к конфликту"""
    model = Documents_conflicts
    form_class = Documents_conflictsForm
    template_name = 'doc_conflict.html'
    success_url = reverse_lazy('doc_conflict')


class Documents_conflictsUpdateView(UpdateView):
    """Обновление списка документов привязанных к конфликтам"""
    model = Documents_conflicts
    form_class = Documents_conflictsForm
    template_name = 'doc_conflict_update.html'
    success_url = reverse_lazy('doc_conflict')


class Documents_conflictsListView(ListView):
    """Список документов привязанных к конфликтам"""
    model = Documents_conflicts
    template_name = 'doc_conflict_update_list.html'
    context_object_name = 'doc_conflict'


class Documents_conflictsView(DeleteView):
    """Удаление привязки документа к конфликту"""
    model = Documents_conflicts
    template_name = 'doc_conflict_delete.html'
    success_url = reverse_lazy('documents_list')


class Document_typeCreateView(CreateView):
    """Добавление типа документа в БД"""
    model = Document_types
    form_class = Document_typesForm
    template_name = 'doc_type.html'
    success_url = reverse_lazy('doc_type')


class Document_typeListView(ListView):
    """Список типов файлов"""
    model = Documents
    template_name = 'documents_list.html'
    context_object_name = 'documents_list'


class DocumentsCreateView(CreateView):
    """Добавление документа в БД"""
    model = Documents
    form_class = DocumentsForm
    template_name = 'document_create.html'
    success_url = reverse_lazy('create_document')


class DocumentsListView(ListView):
    """Список документов"""
    model = Documents
    template_name = 'documents_list.html'
    context_object_name = 'documents_list'


class DocumentsUpdateView(UpdateView):
    """Обновление документа"""
    model = Documents
    form_class = DocumentsForm
    template_name = 'documents_update.html'
    success_url = reverse_lazy('documents_list')


class DocumentsDeleteView(DeleteView):
    """Удаление документов"""
    model = Documents
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
