from django.forms import ModelForm, CharField, PasswordInput

from user.models import User


class UserRegisterForm(ModelForm):
    password1_field_name = "password1"
    password2_field_name = "password2"
    password1 = CharField(
        widget=PasswordInput,
        max_length=128,
        label="Password",
        required=True,
    )

    password2 = CharField(
        widget=PasswordInput,
        max_length=128,
        label="Password (again)",
        required=True,
        help_text="Passwords should be same.",
    )

    class Meta:
        model = User
        fields = ('firstname', 'lastname', 'email')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get(self.password1_field_name)
        password2 = cleaned_data.get(self.password2_field_name)
        if password1 and password1 != password2:
            self.add_error(
                "password2", "You must type the same password each time.")
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
