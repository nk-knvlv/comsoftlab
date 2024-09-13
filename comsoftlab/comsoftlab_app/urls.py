# app_name/urls.py
from django.urls import path
from .views import login_view, register, messages, mail, init_mail

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('mail/init_mail/', init_mail, name='init_mail'),
    path('mail/messages', messages, name='messages'),
    path('mail/', mail, name='mail'),
]
