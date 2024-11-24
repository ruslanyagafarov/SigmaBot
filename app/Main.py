# Main.py
import os
from dotenv import load_dotenv
from TelegramBotService import TelegramBotService
from NotificationService import NotificationService
from TelegramBotHandler import TelegramBotHandler

# Загрузка переменных окружения
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GMAIL_USER = os.getenv("GMAIL_USER")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

# Создание экземпляров сервисов
telegram_bot_handler = TelegramBotHandler()
notification_service = NotificationService(
    smtp_server="smtp.gmail.com",
    smtp_port=587,
    smtp_user=GMAIL_USER,
    smtp_password=MAIL_PASSWORD,
    telegram_bot_handler=telegram_bot_handler
)

# Создание и запуск бота
bot_service = TelegramBotService(TELEGRAM_TOKEN)
bot_service.run()