from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    firstname = forms.CharField(max_length=150, required=True, help_text='Обязательное поле.')
    lastname = forms.CharField(max_length=150, required=True, help_text='Обязательное поле.')

    class Meta:
        model = User
        fields = ('username', 'firstname', 'lastname', 'password1', 'password2')