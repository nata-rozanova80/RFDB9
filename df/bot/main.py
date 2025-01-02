import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, Router, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.types import Update  # Импортируем Update для преобразования вебхука

## Этот адрес нужно вручную менять после перезапуска ngrok
# https://d4c4-2001-41d0-ab05-00-2-0-26b.ngrok-free.app


# Константы
TOKEN = '8164262122:AAG5DlcY1-6pVWkC_-qjXOcQTj22Jd-i7BM'
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://d4c4-2001-41d0-ab05-00-2-0-26b.ngrok-free.app{WEBHOOK_PATH}"  # Укажите актуальный URL от ngrok


BOT_HOST = "127.0.0.1"
BOT_PORT = 8001

# Инициализация бота, хранилища и диспетчера
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Создание роутера
router = Router()


# Обработчики
@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.reply("Привет! Я бот.")


@router.message(Command("status"))
async def order_status_handler(message: types.Message):
    await message.reply("Не удалось найти заказ с таким ключом. Проверьте ключ и попробуйте снова.")


# Обработчик вебхука
async def handle_webhook(request: web.Request):
    try:
        # Получаем JSON-данные от Telegram
        raw_data = await request.json()
        logging.info(f"Получено обновление: {raw_data}")  # Логируем данные

        # Преобразуем данные в объект Update
        update = Update(**raw_data)

        # Передаём обновление диспетчеру
        await dp.feed_update(bot, update)

        #Возвращаем HTTP 200 OK, чтобы Telegram понял, что запрос обработан
        return web.Response(status=200)
    except Exception as e:
        logging.error(f"Ошибка обработки вебхука: {e}")  # Логируем ошибку
        return web.Response(status=500)  # Возвращаем HTTP 500 при ошибке


# Функция для создания и запуска aiohttp-сервера
async def main():
    # Установка вебхука
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"Webhook установлен: {WEBHOOK_URL}")

    # Подключение роутера к диспетчеру
    dp.include_router(router)

    # Создаём AIOHTTP-приложение
    app = web.Application()

    # Регистрируем маршрут для вебхука
    app.router.add_post(WEBHOOK_PATH, handle_webhook)

    # Запуск приложения
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, BOT_HOST, BOT_PORT)
    await site.start()

    logging.info(f"Сервер запущен на {BOT_HOST}:{BOT_PORT}")

    # Бесконечный цикл для работы приложения
    try:
        while True:
            await asyncio.sleep(3600)  # Держим сервер запущенным
    finally:
        await bot.delete_webhook()
        logging.info("Webhook удалён")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

# Временно
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO)
#     asyncio.run(dp.start_polling(bot))
