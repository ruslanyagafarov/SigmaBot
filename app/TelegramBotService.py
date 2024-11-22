from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

class TelegramBotService:
    def __init__(self, token, application_processor):
        self.token = token
        self.processor = application_processor  # Сервис для обработки заявок
        self.application = ApplicationBuilder().token(self.token).build()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start."""
        await update.message.reply_text("Привет! Я бот для обработки заявок.")

    async def process_request(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /process."""
        try:
            self.processor.process_applications()  # Вызываем процессор заявок
            await update.message.reply_text("Обработка заявок завершена успешно!")
        except Exception as e:
            await update.message.reply_text(f"Ошибка обработки: {e}")

    async def check_requests(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /check."""
        try:
            self.processor.process_applications()
            await update.message.reply_text("Обработка заявок завершена успешно!")
        except Exception as e:
            await update.message.reply_text(f"Ошибка обработки: {e}")

    def run(self):
        """Запуск бота."""
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("process", self.process_request))
        self.application.add_handler(CommandHandler("check", self.check_requests))
        self.application.run_polling()
