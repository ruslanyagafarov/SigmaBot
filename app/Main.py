import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv
from GoogleSheetsService import GoogleSheetsService
from NotificationService import NotificationService

# Загрузка переменных окружения
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

# Создание экземпляров сервисов
sheets_service = GoogleSheetsService("credentials.json", GOOGLE_SHEET_ID)
notification_service = NotificationService()


# Функция обработки команды start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Привет! Пожалуйста, отправьте вашу заявку!")


async def process_application(update: Update, context: CallbackContext):
    user_data = update.message.text.split(',')
    if len(user_data) == 5:
        date, name, city, phone, email = map(str.strip, user_data)

        # Получаем список городов филиалов
        branch_cities = sheets_service.get_branch_cities()

        # Проверяем, указан ли город в списке филиалов
        if city not in branch_cities:
            await update.message.reply_text(
                f"К сожалению, в городе {city} нет филиала. Пожалуйста, укажите другой город."
            )
            return

        # Сохраняем заявку в Google Таблицах
        sheets_service.save_application(date, name, city, phone, email)

        # Отправляем уведомление на почту
        notification_service.send_email_to_branch(city, name)

        await update.message.reply_text("Заявка успешно отправлена!")
    else:
        await update.message.reply_text(
            "Пожалуйста, отправьте данные в правильном формате: Дата, ФИО, Город, Телефон, Почта"
        )


# Функция для обработки сообщений (не команд)
async def handle_message(update: Update, context: CallbackContext):
    await update.message.reply_text("Пожалуйста, отправьте вашу заявку в формате: Дата, ФИО, Город, Телефон, Почта")


def main():
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
