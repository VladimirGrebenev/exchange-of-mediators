from django.forms import ModelForm, CharField, PasswordInput, ChoiceField, RadioSelect
from django.utils.translation import gettext_lazy as _

from user.models import User


class UserRegisterForm(ModelForm):
    password1_field_name = "password1"
    password2_field_name = "password2"
    password1 = CharField(
        widget=PasswordInput,
        max_length=128,
        label=_("Пароль"),
        required=True,
    )

    password2 = CharField(
        widget=PasswordInput,
        max_length=128,
        label=_("Ещё раз пароль"),
        required=True,
        help_text=_("Пароли должны совпадать"),
    )

    role = ChoiceField(choices=[('client', 'Клиент'), ('mediator', 'Медиатор')], widget=RadioSelect)

    class Meta:
        model = User
        fields = ('firstname', 'lastname', 'email')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get(self.password1_field_name)
        password2 = cleaned_data.get(self.password2_field_name)
        if password1 and password1 != password2:
            self.add_error(
                "password2", _("Пароли не совпадают"))
        return cleaned_data

    def save(self, *args, **kwargs):
        if (
                "password1" not in self.errors
                and "password2" not in self.errors
                and "password1" in self.changed_data
                and "password2" in self.changed_data
        ):
            self.instance.set_password(self.cleaned_data["password1"])

        return super().save()
