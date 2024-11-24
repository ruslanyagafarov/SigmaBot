# NotificationService.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import logging
from logger_config import setup_logger
from TelegramBotHandler import TelegramBotHandler
import json
from transliterate import translit

logger = setup_logger()

class NotificationService:
    def __init__(self, smtp_server, smtp_port, smtp_user, smtp_password, telegram_bot_handler):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.telegram_bot_handler = telegram_bot_handler
        self.server = None
        self.connect()
        logger.info("NotificationService initialized")

        # Загрузка данных из cities.json
        with open('cities.json', 'r', encoding='utf-8') as file:
            cities_data = json.load(file)
            self.branch_cities = cities_data['cities']
            self.branch_mapping = {city.lower(): city for city in self.branch_cities}

    def connect(self):
        try:
            self.server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            self.server.ehlo()  # Добавляем вызов ehlo() перед starttls()
            self.server.starttls()
            self.server.ehlo()  # Добавляем вызов ehlo() после starttls()
            self.server.login(self.smtp_user, self.smtp_password)
            logger.info("SMTP connection established")
        except Exception as e:
            logger.error(f"Failed to connect to SMTP server: {e}")
            raise

    def send_email_to_branch(self, city, name):
        """Отправка письма на почту филиала."""
        # Транскрипция названия города на английский
        city_translit = translit(city, 'ru', reversed=True).replace(" ", "_").lower()
        recipient_email = f"branch_{city_translit}@example.com"

        message = MIMEMultipart()
        message['From'] = self.smtp_user
        message['To'] = recipient_email
        message['Subject'] = 'New Application'

        body = f'New application: {name} from {city}.'
        message.attach(MIMEText(body, 'plain'))

        try:
            self.server.sendmail(self.smtp_user, recipient_email, message.as_string())
            logger.info(f"Email successfully sent to {recipient_email}")
        except Exception as e:
            logger.error(f"Ошибка при отправке письма: {e}")

    def send_telegram_notification(self, user_id, name, city, experience, phone, email):
        """Отправка уведомления в Telegram-чат."""
        message = f"Новая заявка:\n" \
                  f"Имя: {name}\n" \
                  f"Город: {city}\n" \
                  f"Опыт работы: {experience}\n" \
                  f"Телефон: {phone}\n" \
                  f"Email: {email}"
        self.telegram_bot_handler.send_message(user_id, message)
        logger.info(f"Telegram notification sent for user {user_id}")

    def close(self):
        """Закрытие соединения с SMTP-сервером."""
        if self.server:
            self.server.quit()
            logger.info("NotificationService closed")