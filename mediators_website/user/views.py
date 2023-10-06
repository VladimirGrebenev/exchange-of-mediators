from django.conf import settings
from django.views import View

from .models import EmailConfirmation, Mediator, AdditionalInfo, User

from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from utils.views_mixins import TopFiveMediatorsMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .forms import UserFormProfile, DeleteProfileForm
from conflict.models import Conflict
from reviews.forms import ReviewForm


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
    """
    Отображение списка медиаторов на странице Медиаторы
    """
    model = Mediator
    template_name = 'page-about.html'
    context_object_name = 'mediators_list'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        """
        Отображение полного списка медиаторов внизу страницы
        """
        context = super().get_context_data(**kwargs)
        context['objects_mediators'] = Mediator.objects.all().order_by('lastname')
        context['count_mediators'] = len(context['objects_mediators'])
        # context['objects_mediators'] = Mediator.objects.all()
        return context
    
@login_required
def delete_avatar(request):
    if request.method == 'POST':
        user = request.user

        if user.profile_image:
            # Удаление файла аватара
            user.profile_image.delete(save=False)
            user.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False}, status=400)
    
class DashboardProfileView(View):
    template_name = 'dashboard/page-dashboard-profile.html'

    def get(self, request):
        user = request.user
        profile_form = UserFormProfile(instance=user)
        delete_form = DeleteProfileForm()
        context = {
            'profile_form': profile_form,
            'delete_form': delete_form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user: User = request.user
        profile_form = UserFormProfile(request.POST,request.FILES, instance=user)
        delete_form = DeleteProfileForm(request.POST, instance=user)

        if delete_form.is_valid():
            delete_form.save()
            return redirect('/signing/signout/')

        if profile_form.is_valid():
            profile_form.save()
            update_session_auth_hash(request, user)
            return redirect('/dashboard/profile/')

        messages.add_message(request, messages.ERROR, 'Введены некорректные данные.')

        context = {
            'profile_form': profile_form,
            'delete_form': delete_form,
        }
        return render(request, self.template_name, context)


class ContactTopMediatorsList(TopFiveMediatorsMixin, ListView):
    """
    Отображение списка медиаторов на странице Медиаторы
    """
    model = Mediator
    template_name = 'page-contact.html'
    context_object_name = 'mediators_list'


class MediatorDetailView(DetailView):
    model = Mediator
    template_name = 'user/page-mediator-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReviewForm(initial={'to_user': kwargs['object'].id, 'from_user': self.request.user.id})
        mediator = kwargs['object']
        conflicts = Conflict.objects.filter(mediator=mediator)
        completed_conflicts = conflicts.filter(status='Завершен')
        active_conflicts = conflicts.exclude(status='Завершен')
        context['completed_conflicts'] = completed_conflicts
        context['active_conflicts'] = active_conflicts
        return context

    def post(self, request, *args, **kwargs):
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mediator-detail', kwargs['pk'])
        return render(request, self.template_name, {'form': form})

