# app_name/urls.py
from django.urls import path
from .views import login_view, register, messages, mail

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('messages/<str:is_mail_credentials>/', messages, name='messages_with_param'),  # С параметром
    path('messages/<str:is_mail_credentials>/<str:is_mail_credentials_wrong>/', messages, name='messages_with_params'),
    path('messages/', messages, name='messages'),
    path('mail/', mail, name='mail'),
]
