# SigmaBot - Telegram Bot для обработки заявок

## Описание

**SigmaBot** - это Telegram-бот, разработанный для сбора и обработки заявок от потенциальных сотрудников. Бот задает пользователю серию вопросов, собирает данные и сохраняет их в базе данных. После заполнения анкеты бот отправляет письмо на почту филиала, соответствующего выбранному городу, и уведомляет о новой заявке в Telegram-чат.

## Основные функции

1. **Создание анкеты**: Бот задает пользователю серию вопросов, связанных с его личными данными и предпочтениями для работы.
2. **Отправка письма**: После заполнения анкеты бот автоматически отправляет письмо на почту города, который выбрал пользователь.
3. **Хранение данных**: Все ответы пользователя сохраняются в базе данных SQLite.
4. **Интеграция с Telegram-чатом**: Вся информация о пользователе автоматически отправляется в специальный Telegram-чат.

## Установка и запуск

### 1. Установка зависимостей

Для работы проекта необходим Python 3.7 или выше. Установите зависимости с помощью pip:

```bash
pip install -r requirements.txt
```
### 2. Настройка переменных окружения

Создайте файл .env в корневой директории проекта и добавьте в него следующие строки:
``` plaintext
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
AUTH_TELEGRAM_BOT_TOKEN=your_auth_telegram_bot_token
GMAIL_USER=your_email@gmail.com
MAIL_PASSWORD=your_email_password
GOOGLE_SHEET_ID=your_google_sheet_id
GOOGLE_SHEET_CREDENTIALS=credentials.json
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_email_password
```
Замените your_telegram_bot_token, your_auth_telegram_bot_token, your_email@gmail.com, your_email_password, и your_google_sheet_id на реальные данные.
### 3. Запуск бота

Запустите бота с помощью следующей команды:
``` bash
python Main.py
```

### Структура проекта:

- `TelegramBotService.py:` Основной файл бота, который обрабатывает команды и состояния диалога.

- `DatabaseService.py:` Сервис для работы с базой данных SQLite.

- `NotificationService.py:` Сервис для отправки уведомлений по электронной почте и в Telegram-чат.

- `TelegramBotHandler.py:` Класс для взаимодействия с Telegram Bot API.

- `logger_config.py:` Настройка логгера для проекта.

- `cities.json:` Файл с данными о городах и филиалах.

- `Main.py:` Основной файл для запуска бота.

- `.env:` Файл с переменными окружения.

- `README.md:` Файл с описанием проекта и инструкциями по установке и запуску.

- `credentials.json:` Файл с учетными данными для доступа к Google Sheets API.

