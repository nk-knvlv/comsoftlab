# app_name/urls.py
from django.urls import path
from .views import register, login_view, messages

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('messages/', messages, name='messages'),
]
