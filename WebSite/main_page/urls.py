from django.urls import path
from .views import EmailView, DeleteEmailView

urlpatterns = [
    path('', EmailView.as_view(), name='email_generator'),
    path('delete/', DeleteEmailView.as_view(), name='delete_email'),
]
