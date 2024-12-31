#Теперь run_bot_thread будет запускаться только тогда, когда команда runserver запускает сервер,
# и только после полной инициализации Django.
"""Django's command-line utility for administrative tasks."""
import os
import sys
import threading

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'df.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Импортируем `run_bot_thread` только после инициализации Django
    if 'runserver' in sys.argv:  # Проверяем, запускается ли сервер
        import threading
        from botapp.botapp import run_bot_thread   # Импортируем только при необходимости
        threading.Thread(target=run_bot_thread, daemon=True).start()

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
