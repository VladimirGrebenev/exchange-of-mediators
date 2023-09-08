from django.conf import settings
from django.views.generic import FormView
from django.contrib.auth import login as auth_login, authenticate
from signing.forms import UserRegisterForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect


class SignUpView(FormView):
    form_class = UserRegisterForm
    template_name = 'signing/register.html'
    success_url = settings.SUCCESS_LOGIN_URL

    def form_valid(self, form, **kwargs):
        response = super().form_valid(form)
        user = form.save(commit=False)
        user.save()
        auth_login(self.request, user)
        return response

class SignInUser(LoginView):
    template_name = "signing/login.html"
    # success_message: str = "Signed in."
    # blocked_message: str = 'Account blocked'
    # redirect_authenticated_user = True
    success_url = settings.LOGIN_URL

    def _post(self, request):
        form = self.get_form()
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request=request, username=username, password=password)
            if user is not None:
                # if user.status == Statuses.APPROVED or user.status == Statuses.NEW:
                auth_login(request, user)
                # logger.info(f'Successful login by user {user}')
                return HttpResponseRedirect(self.success_url)
                # else:
                    # logger.warning(f'Unsuccessful login attempt by unapproved user {user}')
                    # form.add_error(None, self.blocked_message)
        # logger.warning(f'Unsuccessfull login attempt from IP {request.META.get("REMOTE_ADDR")}')
        return self.form_invalid(form)

    def post(self, request, *args, **kwargs):
        return self._post(request)
