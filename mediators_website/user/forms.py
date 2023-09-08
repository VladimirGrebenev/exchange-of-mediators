from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Documents, Document_types, Documents_conflicts


class UserForm(UserCreationForm):
    firstname = forms.CharField(max_length=150, required=True, help_text='Обязательное поле.')
    lastname = forms.CharField(max_length=150, required=True, help_text='Обязательное поле.')

    class Meta:
        model = User
        fields = ('username', 'firstname', 'lastname', 'password1', 'password2')


class Documents_conflictsForm(ModelForm):
    """Форма привязки документа к конфликту"""
    class Meta:
        model = Documents_conflicts
        fields = ('document_id', 'conflict_id')


class DocumentsForm(ModelForm):
    """Форма документов(файлов)"""
    class Meta:
        model = Documents
        fields = ('user_id', 'type_id', 'file_path', 'is_all_visible')


class Document_typesForm(ModelForm):
    """Форма типов файлов"""
    class Meta:
        model = Document_types
        fields = ('title',)
