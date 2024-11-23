# Main.py
import os
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv
from GoogleSheetsService import GoogleSheetsService
from NotificationService import NotificationService
import logging
from logger_config import setup_logger

logger = setup_logger()

# Загрузка переменных окружения
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

# Загрузка списка доступных городов из JSON-файла
with open('cities.json', 'r', encoding='utf-8') as file:
    cities_data = json.load(file)
    branch_cities = cities_data['cities']

# Создание экземпляров сервисов
sheets_service = GoogleSheetsService("credentials.json", GOOGLE_SHEET_ID)
notification_service = NotificationService()

# Функция обработки команды start
async def start(update: Update, context: CallbackContext):
    logger.info(f"Received /start command from user {update.message.from_user.id}")
    await update.message.reply_text("Привет! Пожалуйста, отправьте вашу заявку!")

async def process_application(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    message_text = update.message.text

    logger.info(f"Received application from user {user_id} (@{username}, {first_name} {last_name}): {message_text}")

    user_data = message_text.split(',')
    if len(user_data) == 5:
        date, name, city, phone, email = map(str.strip, user_data)

        # Проверяем, указан ли город в списке доступных городов
        if city not in branch_cities:
            logger.warning(f"City {city} not found in branch cities")
            await update.message.reply_text(
                f"К сожалению, в городе {city} нет филиала. Пожалуйста, укажите другой город."
            )
            return

        # Сохраняем заявку в Google Таблицах
        sheets_service.save_application(date, name, city, phone, email)
        logger.info(f"Application saved for user {name} from {city}")

        # Отправляем уведомление на почту
        notification_service.send_email_to_branch(city, name)
        logger.info(f"Notification sent for user {name} from {city}")

        await update.message.reply_text("Заявка успешно отправлена!")
    else:
        logger.warning(f"Invalid application format from user {user_id} (@{username}, {first_name} {last_name}): {message_text}")
        await update.message.reply_text(
            "Пожалуйста, отправьте данные в правильном формате: Дата, ФИО, Город, Телефон, Почта"
        )

# Функция для обработки сообщений (не команд)
async def handle_message(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    message_text = update.message.text

    logger.info(f"Received message from user {user_id} (@{username}, {first_name} {last_name}): {message_text}")
    await update.message.reply_text("Пожалуйста, отправьте вашу заявку в формате: Дата, ФИО, Город, Телефон, Почта")

def main():
    logger.info("Starting bot")
    # Создаем приложение
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))

    # Обработчик сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_application))

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()