from django.forms import ModelForm, CharField, TextInput, EmailInput, DateInput, PasswordInput, ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import models
from .models import User
from django.utils.translation import gettext_lazy as _
from datetime import datetime


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
        fields = ('firstname', 'lastname', 'email', 'phone', 'birthday', 'profile_image')
        widgets = {
            'firstname': TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'lastname': TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
            'phone': TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер телефона'}),
            'birthday': DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'placeholder': 'Дата рождения', 'type': 'date'}),
        }

    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')

        if birthday:
            today = datetime.today().date()
            if birthday > today:
                raise ValidationError('Дата рождения не может быть в будущем')

        return birthday

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
        elif password1 and not password2 or password2 and not password1:
            self.add_error('password2', _('Заполните оба поля'))

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
    
    
class DeleteProfileForm(ModelForm):
    password = CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': '**********'}),
                               required=True)

    class Meta:
        model = User
        fields = []

    def clean_password(self):
        """
        Метод для проверки правильности пароля. Он получает значение пароля
        из очищенных данных формы (`self.cleaned_data.get('password')`) и 
        экземпляр пользователя из атрибута `instance`. Затем он вызывает метод 
        `check_password()` модели `User`, чтобы проверить, совпадает ли хэш пароля 
        с хэшем, хранящимся в базе данных. Если пароль неверный, он вызывает исключение `ValidationError`.
        """
        password = self.cleaned_data.get('password')
        user = self.instance

        if not user.check_password(password):
            raise ValidationError('Неверный пароль')
        return password

    def save(self, commit=True):
        """
         метод для сохранения изменений в модели `User`. 
         Он устанавливает значение `deleted` в `True` для экземпляра 
         пользователя и сохраняет его в базе данных. Если параметр `commit` равен `True`, 
         то изменения будут сохранены в базе данных.
        """
        user = self.instance
        user.deleted = True
        user.deleted_at = datetime.now()

        if commit:
            user.save()
        return user
    