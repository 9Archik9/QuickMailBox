from django.db import models
from django.utils import timezone
from main_page.models import UserEmail


class EmailMessage(models.Model):
    email = models.ForeignKey(UserEmail, on_delete=models.CASCADE)  # Связь с сгенерированной почтой
    api_id = models.IntegerField(unique=True, default=0)  # Уникальный идентификатор сообщения из API
    sender = models.CharField(max_length=255, default=None, db_index=True)  # Email отправителя
    subject = models.CharField(max_length=255, null=True, blank=True, default=None)  # Тема сообщения
    content = models.TextField(null=True, blank=True, default=None)  # Текстовое содержимое сообщения
    html_body = models.TextField(null=True, blank=True, default=None)  # HTML содержимое сообщения
    received_at = models.DateTimeField(default=timezone.now)  # Время получения письма

    def __str__(self):
        return f'From: {self.sender}, Subject: {self.subject}'


class Attachment(models.Model):
    email_message = models.ForeignKey(EmailMessage, related_name='attachments', on_delete=models.CASCADE)
    # Связь с EmailMessage
    filename = models.CharField(max_length=255)  # Имя файла
    content_type = models.CharField(max_length=255)  # расширение содержимого
    size = models.IntegerField()  # Размер файла в байтах

    def __str__(self):
        return self.filename
