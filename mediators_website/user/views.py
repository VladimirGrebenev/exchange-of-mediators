from django.conf import settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash


from .models import EmailConfirmation


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
