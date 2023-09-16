import logging
import uuid
from datetime import datetime, timedelta
from smtplib import SMTPException
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse

from user.models import User, EmailConfirmation

logger = logging.getLogger(__name__)


def send_email(subject: str, message: str, recipient_list: list[str], from_email: str = None):
    if not subject:
        raise ValueError("Subject cannot be empty")
    if not message:
        raise ValueError("Message cannot be empty")
    if not recipient_list:
        raise ValueError("Recipient list cannot be empty")
    from_email = from_email if from_email else settings.DEFAULT_FROM_EMAIL
    try:
        send_mail(subject, message, from_email, recipient_list)
    except SMTPException as e:
        raise ValueError(f"Failed to send email: {str(e)}")


def get_unique_code() -> str:
    confirm_codes = EmailConfirmation.objects.all().values_list('approval_code')
    while True:
        unique_code = uuid.uuid4().hex
        if unique_code not in confirm_codes:
            return unique_code


def send_email_confirmation(request, user: User):
    if not user.email:
        return
    approval_code = get_unique_code()
    subject = 'Email confirmation'
    url = reverse('user:email_confirm', kwargs={'code': approval_code})
    link = f"{request.get_host()}{url}"
    message = f"Thank you for registering on {request.site.name}! Link to email confirmation: {link}"
    exp_date = datetime.now() + timedelta(days=settings.EMAIL_CONFIRM_CODE_TTL_DAYS)
    EmailConfirmation.objects.create(user=user, approval_code=approval_code, code_expiration_date=exp_date)
    send_email(subject, message, [user.email])
