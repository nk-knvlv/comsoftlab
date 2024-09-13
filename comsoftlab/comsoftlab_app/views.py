from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from asyncio import create_task
from django.http import HttpRequest
from .models import Message, Mail
from django.conf import settings
from .services.mail_service import MailService, MailServiceException


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


def mail(request, is_credentials_valid='True'):
    context = {
        'is_credentials_valid': is_credentials_valid
    }
    return render(request, 'mail.html', context)


# Проверяет mail credentials,
# если все в порядке, проверяет есть ли эта почта в бд
# если нет добавляет новую почту
# и перенаправляет на страницу с ее сообщениями
def init_mail(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    print('init_mail begin')
    print(f'email {email}')
    print(f'password {password}')

    if email and password and MailService.is_mail_credentials_valid(email, password):
        print('init_mail all is right')

        if not Mail.objects.filter(mail=email, password=password).exists():
            print('init_mail its new')

            mail_data = {
                'mail': email,
                'password': make_password(password),
                'type': MailService.get_imap_server_by_email(email),
                'last_message_id': None,
            }
            MailService.add_new_mail(mail_data)
        print('init_mail inside')
        return messages(request)
    else:
        return render(request, 'mail.html',
                      {'is_credentials_valid': 'False'})  # перенаправление после успешного входа


@login_required
def messages(request):
    print('messages begin')
    email = request.POST.get('email')
    password = request.POST.get('password')

    context = {
        'email': email
    }

    if Mail.objects.filter(mail=email, password=password).exists():
        stored_messages = Message.objects.all()
        context['stored_messages'] = stored_messages

    return render(request, 'messages.html', context)
