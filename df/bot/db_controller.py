import sqlite3
import logging

# Путь к базе данных (скорректируйте путь в зависимости от расположения)
DB_PATH = "C:\Code\GitHub\Rozanova_final_project\df\db.sqlite3"

def set_user_telegram_id(user_id, telegram_id):
    conn = sqlite3.connect(DB_PATH)

def get_order_status(order_key):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        # Выполняем запрос для получения информации о заказе
        cursor.execute("""
        SELECT o.status, GROUP_CONCAT(b.title || ' x ' || oi.quantity, ', ') AS items
        FROM main_order o
        JOIN main_orderitem oi ON o.id = oi.order_id
        JOIN main_book b ON oi.book_id = b.id
        WHERE o.order_key = ?
        """, parameters=(order_key,))
        result = cursor.fetchone()
        conn.close()

        if result and result[0]:
            return {"status": result[0], "items": result[1]}
        return None
    except sqlite3.Error as e:
        conn.close()
        logging.error(f"Database error: {e}")
        return None
