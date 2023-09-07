from django.conf import settings
from django.views.generic import FormView
from django.contrib.auth import login as auth_login
from signing.forms import UserRegisterForm


class SignInView(FormView):
    form_class = UserRegisterForm
    template_name = 'signing/register.html'
    success_url = settings.SUCCESS_LOGIN_URL

    def form_valid(self, form, **kwargs):
        response = super().form_valid(form)
        user = form.save(commit=False)
        user.save()
        auth_login(self.request, user)
        return response
