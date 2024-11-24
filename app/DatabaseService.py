# DatabaseService.py
import sqlite3
import logging
from logger_config import setup_logger

logger = setup_logger()

class DatabaseService:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()
        logger.info("DatabaseService initialized")

    def create_table(self):
        """Создание таблицы для хранения данных пользователей."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                city TEXT,
                experience TEXT,
                phone TEXT,
                email TEXT,
                status BOOLEAN DEFAULT FALSE
            )
        ''')
        self.conn.commit()
        logger.info("Table 'users' created or already exists")

    def save_user_data(self, user_id, first_name, city, experience, phone, email):
        """Сохранение данных пользователя в базе данных."""
        try:
            self.cursor.execute('''
                INSERT INTO users (user_id, first_name, city, experience, phone, email)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, first_name, city, experience, phone, email))
            self.conn.commit()
            logger.info(f"User data saved for user {user_id}")
        except sqlite3.IntegrityError:
            self.cursor.execute('''
                UPDATE users
                SET first_name = ?, city = ?, experience = ?, phone = ?, email = ?
                WHERE user_id = ?
            ''', (first_name, city, experience, phone, email, user_id))
            self.conn.commit()
            logger.info(f"User data updated for user {user_id}")

    def close(self):
        """Закрытие соединения с базой данных."""
        self.conn.close()
        logger.info("Database connection closed")