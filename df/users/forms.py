# users/forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


User = get_user_model()  # Получаем кастомную модель пользователя

class UserRegisterForm(UserCreationForm):
    telegram_id = forms.CharField(
        required=False,
        label="Telegram ID",
        help_text="Введите ваш Telegram ID для связи."
    )


    class Meta:
        model = User  # Указываем модель пользователя (кастомная или стандартная)
        fields = ['username', 'email', 'password1', 'password2', 'telegram_id']


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Имя",  # Изменённая метка для имени пользователя
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя'}),
    )
    password = forms.CharField(
        label="Пароль",  # Изменённая метка для пароля
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}),
    )