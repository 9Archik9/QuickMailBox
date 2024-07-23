from django.urls import path
from .views import CheckMailView, CheckMailAPI

urlpatterns = [
    path('', CheckMailView.as_view(), name='check_mail_view'),
    path('api/check_mail/', CheckMailAPI.as_view(), name='check_mail_api'),
]
