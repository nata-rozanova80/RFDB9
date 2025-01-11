import asyncio
import logging
import sqlite3
import uuid
import subprocess
from aiohttp import web
from aiogram import Bot, Dispatcher, Router, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.types import Update

# Константы
TOKEN = '8164262122:AAG5DlcY1-6pVWkC_-qjXOcQTj22Jd-i7BM'
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = None  # Установится автоматически через LocalTunnel
DB_PATH = 'C:\\Code\\GitHub\\Rozanova_final_project\\df\\db.sqlite3'
BOT_HOST = "127.0.0.1"
BOT_PORT = 8001

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()
dp.include_router(router)

# Функция для запуска LocalTunnel
def start_localtunnel(port):
    try:
        result = subprocess.run(
            ["lt", "--port", str(port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # Парсим URL из вывода LocalTunnel
        for line in result.stdout.splitlines():
            if "https://" in line:
                return line.strip()
        logging.error("Не удалось получить URL из LocalTunnel")
    except Exception as e:
        logging.error(f"Ошибка запуска LocalTunnel: {e}")
    return None

# Функция получения статуса заказа
def get_order_status(unique_key):
    try:
        uuid.UUID(str(unique_key))  # Проверяем корректность UUID
    except ValueError:
        return None, "Неверный формат уникального ключа."

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.status, GROUP_CONCAT(b.title || ' x ' || oi.quantity, ', ') AS items
                FROM orders_order o
                JOIN orders_orderitem oi ON o.id = oi.order_id
                JOIN catalog_book b ON oi.book_id = b.id
                WHERE o.unique_key = ?
            """, (unique_key,))
            result = cursor.fetchone()

        if not result:
            return None, "Заказ с таким ключом не найден."

        return {"status": result[0], "items": result[1]}, None
    except sqlite3.Error as e:
        logging.error(f"Ошибка базы данных: {e}")
        return None, "Ошибка базы данных."

# Обработчики команд
@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.reply("Привет! Я бот. Используйте команду /status <unique_key>, чтобы узнать статус заказа.")

@router.message(Command("status"))
async def order_status_handler(message: types.Message):
    args = message.text.split()
    if len(args) < 2:
        await message.reply("Пожалуйста, укажите уникальный ключ: /status <unique_key>")
        return

    unique_key = args[1]
    order_status, error = get_order_status(unique_key)

    if error:
        await message.reply(error)
    else:
        await message.reply(
            f"Статус заказа: {order_status['status']}\n"
            f"Товары: {order_status['items']}"
        )

# Обработчик вебхука
async def handle_webhook(request: web.Request):
    try:
        raw_data = await request.json()
        update = Update(**raw_data)
        await dp.feed_update(bot, update)
        return web.Response(status=200)
    except Exception as e:
        logging.error(f"Ошибка обработки вебхука: {e}")
        return web.Response(status=500)

# Основная функция
async def main():
    global WEBHOOK_URL

    # Запуск LocalTunnel и получение публичного URL
    WEBHOOK_URL = start_localtunnel(BOT_PORT)
    if not WEBHOOK_URL:
        logging.error("Не удалось установить соединение через LocalTunnel. Проверьте установку.")
        return

    # Устанавливаем webhook
    await bot.set_webhook(f"{WEBHOOK_URL}{WEBHOOK_PATH}")
    logging.info(f"Webhook установлен: {WEBHOOK_URL}{WEBHOOK_PATH}")

    # Создаём и запускаем AIOHTTP-приложение
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle_webhook)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, BOT_HOST, BOT_PORT)
    await site.start()

    logging.info(f"Сервер запущен на {BOT_HOST}:{BOT_PORT}")

    # Держим приложение запущенным
    try:
        await asyncio.sleep(3600)
    finally:
        await bot.delete_webhook()
        logging.info("Webhook удалён")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
