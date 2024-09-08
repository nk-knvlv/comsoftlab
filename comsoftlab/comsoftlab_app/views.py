from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.http import HttpRequest
from .models import Message


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


def messages(request):
    messages_list = Message.objects.all()
    messages_count = len(messages_list)
    return render(request, 'messages.html', {'messages': messages_list, 'messages_count': messages_count})
