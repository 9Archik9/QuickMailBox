from django.views import View
from django.shortcuts import render, redirect
from core_functionality.main import setup
from core_functionality.delete_mail import delete_mail
from receive_message.models import EmailMessage
from main_page.models import UserEmail


class EmailView(View):
    template_name = 'main_page/email_generator.html'

    def get(self, request):
        # Получаем текущий email, если он есть и не истек
        email_record = UserEmail.objects.filter().first()
        if email_record and email_record.is_expired():
            delete_mail(mail=email_record.email)
            email_record.delete()
            email_record = None

        # Получаем все сообщения
        messages = EmailMessage.objects.filter(email=email_record).order_by('-received_at') if email_record else []

        # Передаем текущий email и сообщения на шаблон
        return render(request, self.template_name, {
            'email': email_record.email if email_record else None,
            'messages': messages
        })

    def post(self, request):
        lifespan = int(request.POST.get('lifespan', 2))  # Получаем выбранное время жизни
        email_record = UserEmail.objects.filter().first()

        # Удаляем старый email, если есть
        if email_record:
            delete_mail(mail=email_record.email)
            email_record.delete()

        # Генерируем новый email и сохраняем его с выбранным временем жизни
        email = setup()
        UserEmail.objects.create(email=email, lifespan_minutes=lifespan)
        return redirect('/')


class DeleteEmailView(View):
    def post(self, request):
        email_record = UserEmail.objects.filter().first()
        if email_record:
            delete_mail(mail=email_record.email)
            email_record.delete()

        return redirect('/')
