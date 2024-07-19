from celery import shared_task
from django.utils import timezone
from .models import UserEmail
from core_functionality.main import delete_mail

@shared_task
def delete_expired_emails():
    now = timezone.now()
    expired_emails = UserEmail.objects.filter(created_at__lt=now - timezone.timedelta(minutes=F('lifespan_minutes')))
    for email in expired_emails:
        delete_mail(mail=email.email)
        email.delete()
