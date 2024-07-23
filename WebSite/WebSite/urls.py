from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_page.urls')),  # основное приложение
    path('receive_message/', include('receive_message.urls')),  # receive_message приложение
]
