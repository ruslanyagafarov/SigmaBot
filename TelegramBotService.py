# TelegramBotService.py
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters, ContextTypes
import logging
from logger_config import setup_logger
import json
from TelegramBotHandler import TelegramBotHandler

logger = setup_logger()

# Состояния для ConversationHandler
NAME, CITY, EXPERIENCE, PHONE, EMAIL, CONFIRM = range(6)

class TelegramBotService:
    def __init__(self, token):
        self.token = token
        self.application = ApplicationBuilder().token(self.token).build()
        logger.info("TelegramBotService initialized")

        # Загрузка данных из cities.json
        with open('cities.json', 'r', encoding='utf-8') as file:
            cities_data = json.load(file)
            self.branch_cities = cities_data['cities']
            self.branch_mapping = {city.lower(): city for city in self.branch_cities}

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start."""
        logger.info(f"Received /start command from user {update.message.from_user.id}")
        await update.message.reply_text("Привет! Я бот для обработки заявок. Пожалуйста, введите ваше имя.")
        return NAME

    async def get_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик ввода имени."""
        context.user_data['name'] = update.message.text
        logger.info(f"Received name: {context.user_data['name']}")
        await update.message.reply_text("Введите ваш город.")
        return CITY

    async def get_city(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик ввода города."""
        city = update.message.text
        if city.lower() not in self.branch_mapping:
            await update.message.reply_text("К сожалению, в этом городе нет филиала. Пожалуйста, введите другой город.")
            return CITY
        context.user_data['city'] = city
        logger.info(f"Received city: {context.user_data['city']}")
        await update.message.reply_text("Введите ваш опыт работы.")
        return EXPERIENCE

    async def get_experience(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик ввода опыта работы."""
        context.user_data['experience'] = update.message.text
        logger.info(f"Received experience: {context.user_data['experience']}")
        await update.message.reply_text("Введите ваш номер телефона.")
        return PHONE

    async def get_phone(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик ввода номера телефона."""
        phone = update.message.text
        if not phone.isdigit() or len(phone) != 11:
            await update.message.reply_text("Пожалуйста, введите корректный номер телефона (11 цифр).")
            return PHONE
        context.user_data['phone'] = phone
        logger.info(f"Received phone: {context.user_data['phone']}")
        await update.message.reply_text("Введите ваш email.")
        return EMAIL

    async def get_email(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик ввода email."""
        email = update.message.text
        if "@" not in email:
            await update.message.reply_text("Пожалуйста, введите корректный email.")
            return EMAIL
        context.user_data['email'] = email
        logger.info(f"Received email: {context.user_data['email']}")
        await update.message.reply_text("Проверьте введенные данные:\n"
                                        f"Имя: {context.user_data['name']}\n"
                                        f"Город: {context.user_data['city']}\n"
                                        f"Опыт работы: {context.user_data['experience']}\n"
                                        f"Телефон: {context.user_data['phone']}\n"
                                        f"Email: {context.user_data['email']}\n"
                                        "Все верно?",
                                        reply_markup=InlineKeyboardMarkup([
                                            [InlineKeyboardButton("Да", callback_data='yes')],
                                            [InlineKeyboardButton("Нет", callback_data='no')]
                                        ]))
        return CONFIRM

    async def confirm(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик подтверждения данных."""
        query = update.callback_query
        await query.answer()
        if query.data == 'yes':
            user_id = update.effective_user.id
            name = context.user_data['name']
            city = context.user_data['city']
            experience = context.user_data['experience']
            phone = context.user_data['phone']
            email = context.user_data['email']

            # Сохранение данных в базе данных
            from DatabaseService import DatabaseService
            db_service = DatabaseService("users.db")
            db_service.save_user_data(user_id, name, city, experience, phone, email)

            # Отправка письма
            from NotificationService import NotificationService
            notification_service = NotificationService(
                os.getenv("SMTP_SERVER"),
                os.getenv("SMTP_PORT"),
                os.getenv("SMTP_USER"),
                os.getenv("SMTP_PASSWORD"),
                TelegramBotHandler()
            )
            notification_service.send_email_to_branch(city, name)

            # Отправка уведомления в Telegram-чат
            notification_service.send_telegram_notification(user_id, name, city, experience, phone, email)

            await query.edit_message_text("Спасибо! Ваша заявка успешно отправлена.")
            return ConversationHandler.END
        else:
            await query.edit_message_text("Пожалуйста, начните заново с команды /start.")
            return ConversationHandler.END

    def run(self):
        """Запуск бота."""
        logger.info("Starting bot")
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", self.start)],
            states={
                NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_name)],
                CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_city)],
                EXPERIENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_experience)],
                PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_phone)],
                EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_email)],
                CONFIRM: [CallbackQueryHandler(self.confirm)]
            },
            fallbacks=[CommandHandler("start", self.start)]
        )
        self.application.add_handler(conv_handler)
        self.application.run_polling()