import datetime

from django import forms
from django.forms import TextInput, Textarea

from conflict.models import Document, Conflict


class ConflictForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ConflictForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['creator'].initial = user

    class Meta:
        model = Conflict
        fields = (
            "title",
            "status",
            "category",
            "mediators_level",
            "prise",
            "fixed_price",
            "decide_time",
            "country",
            "city",
            "language",
            "language_level",
            "mediator",
            "respondents",
            "creator",
            "description",
            "is_all_visible",
        )
        widgets = {
            'creator': forms.HiddenInput(),
            "status": forms.Select({
                'class': "selectpicker",
            }),
            "title": TextInput(attrs={
                'class': "form-control",
                'placeholder': "Текст заголовка",
            }),
            "category": forms.Select({
                'class': "selectpicker",
            }),
            "mediators_level": forms.Select({
                'class': "selectpicker",
            }),
            "prise": forms.Select({
                'class': "selectpicker",
            }),
            "fixed_price": TextInput(attrs={
                'class': "form-control",
                'placeholder': "$",
            }),
            "decide_time": forms.Select({
                'class': "selectpicker",
            }),
            "country": TextInput(attrs={
                'class': "form-control",
                'placeholder': "Страна",
            }),
            "city": TextInput(attrs={
                'class': "form-control",
                'placeholder': "Город",
            }),
            "language": TextInput(attrs={
                'class': "form-control",
                'placeholder': "Язык",
            }),
            "description": Textarea(attrs={
                'cols': "30",
                'rows': "6",
                'class': "form-control",
                'placeholder': "Описание конфликта",
            }),
            "mediator": forms.Select({
                'class': "selectpicker",
            }),
<<<<<<< HEAD
            "respondents": forms.SelectMultiple({
=======
            "respondents": forms.Select({
>>>>>>> e965eed83eef59dd8f9a34ae48dbd184a309db07
                'class': "selectpicker",
            }),
            "is_all_visible": forms.CheckboxInput(attrs={
                'class': "form-check-input",
            })
        }

    def save(self, commit=True):
        conflict = super().save(commit=False)
        # Perform any additional processing or validation here

        if commit:
            conflict.save()
        return conflict


class DocumentForm(forms.ModelForm):

    def __init__(self, user, **kwargs):
        super().__init__(**kwargs)
        self.initial['user'] = user

    class Meta:
        model = Document
        fields = (
            "file_path",
            "user",
            "is_all_visible",
        )
        widgets = {
            "user": forms.HiddenInput,
        }
