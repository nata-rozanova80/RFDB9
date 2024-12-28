# botapp.py
from django.utils import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from django.conf import settings

# Обработчик команды /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Я бот для доставки цветов. Чем могу помочь?')

# Обработчик команды /help
async def help(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Используй команды:\n/start - чтобы начать\n/help - для помощи')

# Функция для запуска бота
async def run_bot():
    application = Application.builder().token(settings.TELEGRAM_BOT_API_KEY).build()

    # Добавление обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))

    # Запуск бота
    await application.run_polling()

# Для запуска в отдельном потоке
def run_bot_thread():
    # Получаем существующий цикл событий
    loop = asyncio.get_event_loop()

    # Запускаем асинхронную задачу в существующем цикле событий
    loop.create_task(run_bot())