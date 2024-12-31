# users/models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.contrib.auth.models import User  # Импорт модели User из Django
from django.conf import settings  # Импортируем настройки проекта

class User(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions_set')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    email = models.EmailField(unique=True)
    telegram_id = models.CharField(max_length=50, blank=True, null=True, unique=True, verbose_name="Telegram ID")

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # Указываем связь через AUTH_USER_MODEL
        on_delete=models.CASCADE,
        related_name='profile'
    )
    telegram_id = models.CharField(max_length=50, blank=True, null=True, unique=True, verbose_name="Telegram ID")

    def __str__(self):
        return self.user.username

# class CustomUser(AbstractUser):
#     groups = models.ManyToManyField(Group, related_name='custom_user_set')
#     user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions_set')
#     phone = models.CharField(max_length=15, blank=True)
#     address = models.TextField(blank=True)
#     email = models.EmailField(unique=True)
#     telegram_id = models.CharField(max_length=50, blank=True, null=True, unique=True, verbose_name="Telegram ID")


    def __str__(self):
        return self.username


