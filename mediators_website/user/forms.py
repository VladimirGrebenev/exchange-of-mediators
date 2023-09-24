from django.forms import ModelForm, CharField, TextInput, EmailInput, DateInput, PasswordInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import models
from .models import User
from django.utils.translation import gettext_lazy as _


class UserForm(UserCreationForm):
    firstname = CharField(max_length=150, required=True, help_text='Обязательное поле.')
    lastname = CharField(max_length=150, required=True, help_text='Обязательное поле.')

    class Meta:
        model = models.User
        fields = ('username', 'firstname', 'lastname', 'password1', 'password2')


class UserFormProfile(ModelForm):
    password1_field_name = "password1"
    password2_field_name = "password2"
    password1 = CharField(
        widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': '**********'}),
        max_length=128,
        required=False
    )

    password2 = CharField(
        widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': '**********'}),
        max_length=128,
        required=False,
        help_text=_("Пароли должны совпадать"),
    )
    class Meta:
        model = User
        fields = ('firstname', 'lastname', 'email', 'phone', 'birthday',)
        widgets = {
            'firstname': TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'lastname': TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
            'phone': TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер телефона'}),
            'birthday': DateInput(attrs={'class': 'form-control', 'placeholder': 'День рождения'}),
        }

    def clean(self):
        """
        Метод, который выполняет дополнительную валидацию формы после основной валидации. 
        В данном случае, он проверяет, что значения полей `password1` и `password2` совпадают. 
        Если они не совпадают, добавляется ошибка ниже поля `password2` с сообщением "Пароли не совпадают".
        """
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', _('Пароли не совпадают'))

        return cleaned_data

    def save(self, *args, **kwargs):
        """
        Метод, который сохраняет данные формы. Если поля пароля не содержат ошибок
        и были изменены, то пароль пользователя устанавливается в значение поля `password1`. 
        Затем вызывается метод `save()` для сохранения экземпляра модели `User`
        """
        if self.cleaned_data.get('password1'):
            self.instance.set_password(self.cleaned_data['password1'])
        return super().save(*args, **kwargs)
    