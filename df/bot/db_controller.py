# bot/db_controller.py


import sqlite3
import logging

# Путь к базе данных (скорректируйте путь в зависимости от расположения)
DB_PATH = "C:\Code\GitHub\Rozanova_final_project\df\db.sqlite3"

def get_user_and_order_status(order_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        # Выполняем запрос для получения Telegram ID пользователя и статуса заказа
        cursor.execute("""
        SELECT u.telegram_id, o.unique_key, o.status
        FROM users_user u
        JOIN orders_order o ON u.id = o.user_id
        WHERE o.id = ?
        """, (order_id,))
        result = cursor.fetchone()
        return result  # Вернём результат запроса
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
        return None
    finally:
        conn.close()


def set_user_telegram_id(user_id, telegram_id, unique_key):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        # Выполняем запрос для обновления Telegram ID в таблице users_user
        cursor.execute("""
           UPDATE users_user
           SET telegram_id = ?
           WHERE id = (
               SELECT user_id
               FROM orders_order
               WHERE unique_key = ?
           )
           """, (telegram_id, unique_key))  # Заменяем order_key на unique_key
        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
    finally:
        conn.close()


def get_order_status(unique_key):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        # Выполняем запрос для получения информации о заказе
        cursor.execute("""
        SELECT o.status, GROUP_CONCAT(b.title || ' x ' || oi.quantity, ', ') AS items
        FROM orders_order o
        JOIN orders_orderitem oi ON o.id = oi.order_id
        JOIN catalog_book b ON oi.book_id = b.id
        WHERE o.unique_key = ?
        """, (unique_key,))
        result = cursor.fetchone()
        conn.close()

        if result and result[0]:
            return {"status": result[0], "items": result[1]}
        return None
    except sqlite3.Error as e:
        conn.close()
        logging.error(f"Database error: {e}")
        return None


        if result and result[0]:
            return {"status": result[0], "items": result[1]}
        return None
    except sqlite3.Error as e:
        conn.close()
        logging.error(f"Database error: {e}")
        return None
