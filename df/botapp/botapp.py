# botapp.py
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from django.conf import settings


# Обработчик команды /start
async def start(update: Update, context: CallbackContext) -> None:
    telegram_id = update.message.chat.id
    user = CustomUser.objects.filter(telegram_id=str(telegram_id)).first()

    if user:
        await update.message.reply_text(f"Привет, {user.username}! Чем могу помочь?")
    else:
        await update.message.reply_text(
            "Привет! Похоже, вы ещё не зарегистрированы. Пожалуйста, зарегистрируйтесь на сайте и укажите ваш Telegram ID."
        )

def get_order_model():
    from orders.models import Order
    return Order

def get_user_model():
    from users.models import CustomUser
    return CustomUser


# Обработчик команды /help
async def help(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Используй команды:\n/start - чтобы начать\n/help - для помощи')


async def get_order_status(update: Update, context: CallbackContext) -> None:
    try:
        # Получение ключа из сообщения пользователя
        Order = get_order_model()
        user_input = context.args[0]
        order = Order.objects.get(unique_key=user_input)

        # Проверка, совпадает ли telegram_id клиента
        telegram_id = update.message.chat.id
        if order.user.telegram_id == str(telegram_id):
            await update.message.reply_text(f"Статус вашего заказа: {order.status}")
        else:
            await update.message.reply_text("Вы не авторизованы для просмотра этого заказа.")
    except IndexError:
        await update.message.reply_text("Пожалуйста, укажите ключ заказа. Пример: /status <ключ>")
    except Order.DoesNotExist:
        await update.message.reply_text("Заказ с указанным ключом не найден.")
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка: {e}")


# Функция для запуска бота
async def run_bot():
    application = Application.builder().token(settings.TELEGRAM_BOT_API_KEY).build()

    # Добавление обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("status", get_order_status))

    # Запуск бота
    await application.run_polling()

# Для запуска в отдельном потоке
def run_bot_thread():
    # Получаем существующий цикл событий
    loop = asyncio.get_event_loop()

    # Запускаем асинхронную задачу в существующем цикле событий
    loop.create_task(run_bot())