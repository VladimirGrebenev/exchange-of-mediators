from django.conf import settings
from django.contrib.auth.models import Group
from django.views.generic import FormView
from django.contrib.auth import login as auth_login, authenticate
from signing.forms import UserRegisterForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.contrib import messages


class SignupView(FormView):
    form_class = UserRegisterForm
    template_name = 'signing/register.html'
    success_url = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form, **kwargs):
        response = super().form_valid(form)
        user = form.save(commit=False)
        if form.cleaned_data.get('role') == 'mediator':
            group_name = 'mediator'
        else:
            group_name = 'user'

        new_group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.set([new_group])
        user.save()
        auth_login(self.request, user)
        messages.success(self.request, 'Аккаунт успешно создан')

        return response


class SigninView(LoginView):
    template_name = "signing/login.html"
    redirect_authenticated_user = True
    success_url = settings.LOGIN_REDIRECT_URL

    def _post(self, request):
        form = self.get_form()
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request=request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return HttpResponseRedirect(self.success_url)
        return self.form_invalid(form)

    def post(self, request, *args, **kwargs):
        return self._post(request)


class SignoutView(LogoutView):
    pass
