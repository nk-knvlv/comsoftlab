# app_name/urls.py
from django.urls import path
from .views import login_view, register, messages, mail

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('mail/messages/', messages, name='messages'),
    path('mail/', mail, name='mail'),
]
