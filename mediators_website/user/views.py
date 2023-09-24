from django.conf import settings
from django.views import View
from django.views.generic import ListView

from .models import EmailConfirmation, Mediator, AdditionalInfo, User

from django.views.generic import FormView, ListView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from utils.views_mixins import TopFiveMediatorsMixin


from .models import EmailConfirmation
from .forms import UserFormProfile
from user.models import Mediator


class EmailConfirmView(View):
    def get(self, request, code):
        try:
            email = EmailConfirmation.objects.get(approval_code=code)
        except EmailConfirmation.DoesNotExist:
            messages.error(request, 'Something went wrong, try again and contact with technicals')
        else:
            email.is_approved = True
            email.save()
            messages.success(request, 'Mail has been successfully confirmed')
        return redirect(settings.LOGIN_URL)


class TopMediatorsList(TopFiveMediatorsMixin, ListView):
    model = Mediator
    template_name = 'page-about.html'
    context_object_name = 'mediators_list'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objects_mediators'] = Mediator.objects.all()
        print(context)
        print(context['objects_mediators'])
        return context


class DashboardProfileView(FormView):
    """
    Представление на основе `FormView` для отображения и обработки
    профиля пользователя
    """
    template_name = 'dashboard/page-dashboard-profile.html'

    def get(self, request):
        """
        Mетод отображает форму профиля пользователя при GET-запросе. 
        Он создает экземпляр формы `UserFormProfile` с текущим пользователем и 
        передает его в контекст шаблона для отображения.
        """
        user = request.user
        profile_form = UserFormProfile(instance=user)
        context = {
            'profile_form': profile_form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user
        profile_form = UserFormProfile(request.POST, instance=user)

        if profile_form.is_valid():
            """
            Mетод обрабатывает форму профиля пользователя при POST-запросе. 
            Он создает экземпляр формы `UserFormProfile` с данными из запроса и 
            текущим пользователем. Если форма проходит валидацию, 
            данные сохраняются, сессия аутентификации обновляется, 
            и пользователь перенаправляется на указанный URL
            """
            profile_form.save()
            update_session_auth_hash(request, user)
            return redirect('/dashboard/user/')
        
        else:
            context = {
                'profile_form': profile_form,
            }
        return render(request, self.template_name, context)
