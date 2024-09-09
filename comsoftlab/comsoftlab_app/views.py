from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.http import HttpRequest
from .models import Message, Mail
from django.conf import settings
from .services.mail_service import MailService


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # перенаправление на страницу входа
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    # request.POST['is_credentials_wrong'] = False
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('messages')  # перенаправление после успешного входа
        else:
            is_credentials_wrong = True
            return render(request, 'login.html', {'is_credentials_wrong': is_credentials_wrong})
    return render(request, 'login.html')


def messages(request, is_mail_credentials='False', is_mail_credentials_wrong='False'):
    mail_service_settings = {
        'mail_pass': settings.MAIL_SERVICE_CONF['mail_pass'],
        'imap_server': settings.MAIL_SERVICE_CONF['imap_server'],
    }
    mail_service = MailService(request, mail_service_settings)
    # messages_count = mail_service.get_messages_count()
    messages_count = 4

    messages_list = Message.objects.all()
    return render(request, 'messages.html', {'messages': messages_list, 'messages_count': request.user.username,
                                             'is_mail_credentials': is_mail_credentials, 'is_mail_credentials_wrong': is_mail_credentials_wrong})


def mail(request):
    # mail_list = Mail.objects.all()
    email = request.POST.get('email')
    password = request.POST.get('password')
    match email:
        case email if '@yandex' in email:
            mail_type = 'yandex'
        case email if '@gmail' in email:
            mail_type = 'gmail'
        case _:
            mail_type = 'mail'

    # Создание нового объекта
    try:
        new_mail = Mail(mail=email, password=password, type=mail_type, last_message_id='None')
    except Exception:
        return redirect('messages_with_params', {'is_mail_credentials': 'False',
                                                 'is_mail_credentials_wrong': 'True'})  # перенаправление после успешного входа
    new_mail.save()  # Сохранение объекта в БД
    return redirect('messages_with_param', {'is_mail_credentials': 'True'})  # перенаправление после успешного входа
