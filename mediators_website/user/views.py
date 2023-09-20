from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView

from .models import EmailConfirmation, Mediator
from utils.views_mixins import TopFiveMediatorsMixin


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
