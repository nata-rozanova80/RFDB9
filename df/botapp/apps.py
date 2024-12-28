# botapp/apps.py моего Django приложения

from django.apps import AppConfig
import threading
from .botapp import run_bot_thread  # Импорт функции для запуска бота

class BotAppConfig(AppConfig):
    name = 'botapp'

    def ready(self):
        # Запуск бота в отдельном потоке при старте Django
        threading.Thread(target=run_bot_thread).start()