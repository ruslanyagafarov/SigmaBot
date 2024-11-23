# TelegramBotService.py
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import logging
from logger_config import setup_logger

logger = setup_logger()

class TelegramBotService:
    def __init__(self, token, application_processor):
        self.token = token
        self.processor = application_processor  # Сервис для обработки заявок
        self.application = ApplicationBuilder().token(self.token).build()
        logger.info("TelegramBotService initialized")

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start."""
        logger.info(f"Received /start command from user {update.message.from_user.id}")
        await update.message.reply_text("Привет! Я бот для обработки заявок.")

    async def process_request(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /process."""
        logger.info(f"Received /process command from user {update.message.from_user.id}")
        try:
            self.processor.process_applications()  # Вызываем процессор заявок
            await update.message.reply_text("Обработка заявок завершена успешно!")
        except Exception as e:
            logger.error(f"Error processing applications: {e}")
            await update.message.reply_text(f"Ошибка обработки: {e}")

    async def check_requests(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /check."""
        logger.info(f"Received /check command from user {update.message.from_user.id}")
        try:
            self.processor.process_applications()
            await update.message.reply_text("Обработка заявок завершена успешно!")
        except Exception as e:
            logger.error(f"Error processing applications: {e}")
            await update.message.reply_text(f"Ошибка обработки: {e}")

    def run(self):
        """Запуск бота."""
        logger.info("Starting bot")
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("process", self.process_request))
        self.application.add_handler(CommandHandler("check", self.check_requests))
        self.application.run_polling()