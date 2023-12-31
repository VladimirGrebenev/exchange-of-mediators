from django.conf import settings

from django.middleware.csrf import get_token

from django.urls import reverse

from django.views import View

from .models import EmailConfirmation, Mediator, User, ContactMessage
from reviews.models import Review

from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.views_mixins import TopFiveMediatorsMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count

from .forms import UserFormProfile, DeleteProfileForm, ContactMessageForm
from conflict.models import Conflict
from reviews.forms import ReviewForm

LEVEL_MESSAGE = 50


class EmailConfirmView(View):
    def get(self, request, code):
        try:
            email = EmailConfirmation.objects.get(approval_code=code)
        except EmailConfirmation.DoesNotExist:
            messages.error(request, 'Что-то пошло не так, попробуйте еще раз и обратитесь в службу технической поддержки', extra_tags='danger')
        else:
            email.is_approved = True
            email.save()
            messages.success(request, 'Почта успешно подтверждена')
        return redirect(settings.LOGIN_URL)


class TopMediatorsList(TopFiveMediatorsMixin, ListView):
    """
    Отображение списка медиаторов на странице Медиаторы
    """
    model = Mediator
    template_name = 'page-about.html'
    context_object_name = 'mediators_list'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        """
        Отображение полного списка медиаторов внизу страницы
        """
        context = super().get_context_data(**kwargs)
        context['objects_mediators'] = Mediator.objects.all().order_by('lastname')
        context['count_mediators'] = len(context['objects_mediators'])

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
    
    
class DashboardProfileView(LoginRequiredMixin, View):
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

            if 'password1' in request.POST and request.POST['password1'] != '' and request.POST['password2'] != '':
                messages.success(request, 'Пароль успешно изменен.')
            else:
                messages.success(request, 'Данные профиля успешно изменены.')

            profile_form.save()
            update_session_auth_hash(request, user)

        else:
            messages.error(request, 'Введены некорректные данные.', extra_tags='danger')

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
    

class MediatorAboutView(DetailView):
    model = Mediator
    template_name = 'user/page-mediator-about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReviewForm(initial={'to_user': kwargs['object'].id, 'from_user': self.request.user.id})
        mediator = kwargs['object']
        mediator_id = mediator.id
        reviews = Review.objects.filter(to_user_id=mediator_id)

        quantity_reviews = reviews.count()

        ratings = reviews.values('rating').annotate(count=Count('rating')).order_by('rating')
        total_reviews = reviews.count()

        star_counts = {5: {'count': 0, 'percentage': 0},
                       4: {'count': 0, 'percentage': 0},
                       3: {'count': 0, 'percentage': 0},
                       2: {'count': 0, 'percentage': 0},
                       2: {'count': 0, 'percentage': 0},
                       1: {'count': 0, 'percentage': 0},
                       }

        star_counts_up = {rating['rating']: {
            'count': rating['count'],
            'percentage': (rating['count'] / total_reviews) * 100
        } for rating in ratings}
        star_counts.update(star_counts_up)

        conflicts = Conflict.objects.filter(mediator=mediator)
        completed_conflicts = conflicts.filter(status='Завершен').count()
        total_conflicts = conflicts.filter(mediator_id=mediator).count()
        active_conflicts = conflicts.exclude(status='Завершен')

        context.update({
            'reviews': reviews,
            'quantity_reviews': quantity_reviews,
            'completed_conflicts': completed_conflicts,
            'active_conflicts': active_conflicts,
            'total_conflicts': total_conflicts,
            'star_counts': star_counts,
        })

        return context

    def get_success_url(self):
        return self.request.path

    def post(self, request, *args, **kwargs):
        form = ReviewForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('from_user')
            mediator = form.cleaned_data.get('to_user')
            if user == mediator:
                messages.error(request, 'Вы не можете оставить отзыв о себе', extra_tags='danger')
            elif user.groups.first().name == 'mediator':
                messages.error(request, 'Вы не можете оставить отзыв о другом медиаторе', extra_tags='danger')
            elif mediator.reviews.filter(from_user=user).count() > 0:
                messages.info(request, 'Вы уже оставили отзыв')
            else:
                form.save()
                messages.success(request, 'Ваш отзыв учтен')
                return redirect(reverse('reviews:list_review'))
            return redirect(self.get_success_url())
        else:
            messages.error(request, 'Ошибка заполнения формы', extra_tags='danger')

            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            context['form'] = form
            return render(request, self.template_name, context=context)


class ClientAboutView(DetailView):
    model = User
    template_name = 'user/page-user-about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client'] = context['user']  # Заменяем имя переменной user на client
        del context['user']  # Удаляем переменную user из контекста
        return context


class ContactMessageView(View):
    model = ContactMessage
    template_name = 'page-contact.html'
    # context_object_name = 'contacts-message'

    def get(self, request):
        form = ContactMessageForm()
        return render(request, 'page-contact.html', {'form': form})

    def post(self, request):
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваше сообщение успешно отправлено.')
            print("Имя: ", form.cleaned_data['name'])
            print("email: ", form.cleaned_data['email'])
            print("message: ", form.cleaned_data['message'])
            return redirect('contacts')  # Перенаправляем на страницу контактов
        else:
            messages.error(request, 'Произошла ошибка в отправке формы. Пожалуйста, проверьте данные и попробуйте ещё раз.')
        return render(request, 'page-contact.html', {'form': form, 'csrf_token': get_token(request)})
