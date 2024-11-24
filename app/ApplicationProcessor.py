import os
from GoogleSheetsService import GoogleSheetsService
from NotificationService import NotificationService


class ApplicationProcessor:
    def __init__(self):
        # Инициализация сервисов
        self.sheets_service = GoogleSheetsService("credentials.json", os.getenv("GOOGLE_SHEET_ID"))
        self.notification_service = NotificationService()

    def process_application(self, update):
        # Получаем данные из сообщения
        user_data = update.message.text.split(',')

        if len(user_data) == 5:
            date, name, city, phone, email = user_data

            # Сохраняем заявку в Google Таблицах
            self.sheets_service.save_application(date, name, city, phone, email)

            # Отправляем уведомление на почту
            self.notification_service.send_email_to_branch(city, name)

            update.message.reply_text("Заявка успешно отправлена!")
        else:
            update.message.reply_text(
                "Пожалуйста, отправьте данные в правильном формате: Дата, ФИО, Город, Телефон, Почта")
