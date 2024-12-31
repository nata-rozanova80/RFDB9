from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    telegram_id = models.CharField(max_length=50, blank=True, null=True, unique=True, verbose_name="Telegram ID")

    def __str__(self):
        return self.user.username
