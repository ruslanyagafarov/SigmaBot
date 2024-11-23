# TelegramBotHandler.py
from dotenv import load_dotenv
import os
import requests
import logging
from logger_config import setup_logger

logger = setup_logger()

# Загрузка переменных окружения
load_dotenv()

class TelegramBotHandler:
    """Класс для взаимодействия с Telegram Bot API."""

    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")  # Читаем токен из переменной окружения
        if not self.token:
            logger.error("Telegram Bot Token не найден. Проверьте файл .env.")
            raise ValueError("Telegram Bot Token не найден. Проверьте файл .env.")
        self.api_url = f"https://api.telegram.org/bot{self.token}"
        logger.info("TelegramBotHandler initialized")

    def send_message(self, chat_id, message):
        """Отправляет сообщение через бот."""
        logger.info(f"Sending message to chat {chat_id}: {message}")
        url = f"{self.api_url}/sendMessage"
        payload = {"chat_id": chat_id, "text": message}
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            logger.error(f"Ошибка отправки сообщения: {response.text}")
            raise Exception(f"Ошибка отправки сообщения: {response.text}")