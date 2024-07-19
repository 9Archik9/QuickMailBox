from celery import shared_task
from django.utils import timezone
from .models import UserEmail
from core_functionality.delete_mail import delete_mail


@shared_task #  декоратор, который используется для определения задач (tasks),
# которые могут быть выполнены асинхронно с помощью Celery.
def delete_expired_emails(): #  функция определяет задачу, которая будет выполнена Celery для удаления устаревших email
    now = timezone.now() #  получение текущего времени
    expired_emails = UserEmail.objects.filter(created_at__lt=now - timezone.timedelta(minutes=10))
    # использя ORM Django фильтруем записи в таблице UserEmail, созданные более 10 минут назад
    for email in expired_emails:
        delete_mail(mail=email.email)
        email.delete()
