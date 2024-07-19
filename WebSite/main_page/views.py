from django.views import View
from django.shortcuts import render, redirect
from django.utils import timezone
from core_functionality.main import setup, delete_mail
from .models import UserEmail


class EmailView(View):
    template_name = 'main_page/email_generator.html'

    def get(self, request):
        email_record = UserEmail.objects.filter().first()
        if email_record:
            if email_record.is_expired():
                delete_mail(mail=email_record.email)
                email_record.delete()
                email_record = None

        if not email_record:
            email = setup()
            email_record = UserEmail.objects.create(email=email)

        return render(request, self.template_name, {'email': email_record.email})

    def post(self, request):
        email_record = UserEmail.objects.filter().first()
        if email_record:
            delete_mail(mail=email_record.email)
            email_record.delete()

        email = setup()
        UserEmail.objects.create(email=email)
        return redirect('/')


class DeleteEmailView(View):
    def post(self, request):
        email_record = UserEmail.objects.filter().first()
        if email_record:
            delete_mail(mail=email_record.email)
            email_record.delete()

        return redirect('/')
