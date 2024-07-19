from django.db import models
from django.utils import timezone
import datetime


class UserEmail(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    lifespan_minutes = models.IntegerField(default=2)  # Время жизни email в минутах

    def is_expired(self):
        return timezone.now() > self.created_at + datetime.timedelta(minutes=self.lifespan_minutes)
