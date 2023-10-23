import datetime
from django import forms
from django.forms import TextInput, Textarea
from django.shortcuts import redirect

from conflict.models import Document, Conflict, ConflictResponse

from user.models import BasicUser, User
from django.db.models import Q


class ConflictForm(forms.ModelForm):

    class Meta:
        model = Conflict
        fields = (
            "status",
            "creator",
            "mediator",

            "title",
            "category",
            # "mediators_level",
            # "prise",
            "fixed_price",
            "decide_time",
            "country",
            "city",
            # "language",
            # "language_level",
            # "respondents",
            "description",
            # "is_all_visible",
        )
        widgets = {
            "status": forms.HiddenInput(),
            'creator': forms.HiddenInput(),
            'mediator': forms.HiddenInput(),

            "title": TextInput(attrs={
                'class': "form-control",
                'placeholder': "Текст заголовка",
            }),
            "category": forms.Select({
                'class': "selectpicker",
            }),
            # "mediators_level": forms.Select({
            #     'class': "selectpicker",
            # }),
            # "prise": forms.Select({
            #     'class': "selectpicker",
            # }),
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
            # "language": TextInput(attrs={
            #     'class': "form-control",
            #     'placeholder': "Язык",
            # }),
            "description": Textarea(attrs={
                'cols': "30",
                'rows': "6",
                'class': "form-control",
                'placeholder': "Описание конфликта",
            }),
            # "mediator": forms.Select({
            #     'class': "selectpicker",
            # }),
            # "respondents": forms.SelectMultiple({
            #     'class': "selectpicker",
            # }),
            # "is_all_visible": forms.CheckboxInput(attrs={
            #     'class': "form-check-input",
            # })
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


class ResponseForm(forms.ModelForm):

    def clean_rate(self):
        rate = self.cleaned_data.get('rate')
        fixed_price = self.cleaned_data.get('conflict').fixed_price
        if rate < fixed_price:
            raise forms.ValidationError('Цена должна быть не ниже заявленной')
        return rate

    class Meta:
        model = ConflictResponse
        fields = [
            "conflict",
            "mediator",
            "rate",
            "time_for_conflict",
            "comment"
        ]
        widgets = {
            "conflict": forms.HiddenInput,
            "mediator": forms.HiddenInput,
            "rate": forms.NumberInput(attrs={"placeholder": f"Цена не ниже заявленной", "class": "form-control"}),
            "time_for_conflict": forms.NumberInput(attrs={"placeholder": "Количество дней", "class": "form-control"}),
            "comment": forms.Textarea(
                attrs={
                    "rows": 6,
                    "style": "height: 100%",
                    "placeholder": "Пара слов заявителю...",
                    "class": "form-control",
                }
            ),
        }


class ResponseUserForm(forms.ModelForm):
    class Meta:
        model = Conflict
        fields = [
            "category",
            "mediator",
            "fixed_price",
            "decide_time",
        ]
        widgets = {
            "category": forms.HiddenInput,
            "mediator": forms.HiddenInput,
            "fixed_price": forms.HiddenInput,
            "decide_time": forms.HiddenInput,
        }


class RespondentsForm(forms.ModelForm):
    class Meta:
        model = Conflict
        fields = ['respondents']
        widgets = {
            "respondents": forms.SelectMultiple(
                attrs={"placeholder": "Выберите пользователей", "class": "selectpicker"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['respondents'].queryset = BasicUser.objects.exclude(id__in=self.instance.respondents.all())

