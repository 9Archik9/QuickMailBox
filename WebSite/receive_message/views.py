from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from main_page.models import UserEmail
from .models import EmailMessage
from core_functionality.check_mail import check_mail
from django.utils.dateformat import format


class CheckMailView(View):
    def get(self, request, *args, **kwargs):
        emails = EmailMessage.objects.all()  # Или ваш фильтр для получения новых сообщений
        email_data = []

        for email in emails:
            email_data.append({
                'sender': email.sender,
                'subject': email.subject,
                'content': email.content,
                'date': email.received_at.strftime('%H:%M')  # Форматирование даты
            })

        return JsonResponse({'messages': email_data})


class CheckMailAPI(View):
    def get(self, request):
        try:
            user_email = UserEmail.objects.latest('created_at')
            email_messages = check_mail(mail=user_email.email)

            for message in email_messages:
                # Обрабатываем данные сообщения и сохраняем в базу данных
                EmailMessage.objects.get_or_create(
                    email=user_email,
                    api_id=message.get('api_id'),  # Используем get для избежания KeyError
                    defaults={
                        'sender': message.get('sender'),
                        'subject': message.get('subject'),
                        'content': message.get('content'),
                        'received_at': timezone.now(),
                    }
                )

            # Возвращаем сообщения, привязанные к текущему пользователю
            messages = EmailMessage.objects.filter(email=user_email)
            data = [{'sender': msg.sender, 'subject': msg.subject, 'date': msg.received_at, 'content': msg.content} for msg in messages]
            return JsonResponse({'messages': data})
        except UserEmail.DoesNotExist:
            return JsonResponse({'messages': []})

