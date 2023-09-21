from django.conf import settings
from django.views import View
<<<<<<< HEAD
<<<<<<< HEAD
from django.views.generic import ListView

from .models import EmailConfirmation, Mediator
from utils.views_mixins import TopFiveMediatorsMixin
=======
=======
>>>>>>> 36e16bcdae6388a87ec18ad434983ae50d160463
from django.views.generic import FormView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash


from .models import EmailConfirmation
from .forms import UserFormProfile
<<<<<<< HEAD
>>>>>>> 36e16bc (added the ability to edit profile)
=======
>>>>>>> 36e16bcdae6388a87ec18ad434983ae50d160463


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


<<<<<<< HEAD
<<<<<<< HEAD
class TopMediatorsList(TopFiveMediatorsMixin, ListView):
    model = Mediator
    template_name = 'page-about.html'
    context_object_name = 'mediators_list'
=======
=======
>>>>>>> 36e16bcdae6388a87ec18ad434983ae50d160463
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
<<<<<<< HEAD
    
>>>>>>> 36e16bc (added the ability to edit profile)
=======
    
>>>>>>> 36e16bcdae6388a87ec18ad434983ae50d160463
