# users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm

class CustomLoginView(LoginView):
    template_name = 'users/login.html'  # Путь к кастомному шаблону

def my_logout(request):
    logout(request)
    messages.success(request, "Вы удачно вышли из системы.")
    return redirect('index')

# Что делает этот код:
#
# logout(request) — выходит из учётной записи пользователя.
# messages.success() — устанавливает сообщение об успешном выходе.
# redirect('index') — перенаправляет на маршрут с именем index.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно! Добро пожаловать.")
            return redirect('index')
        else:
            messages.error(request, "Произошла ошибка при регистрации. Пожалуйста, исправьте ошибки ниже.")
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
