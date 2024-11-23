# application_handler.py
import re
from datetime import datetime
from states import ApplicationStates
from database import save_answer, mark_complete

def validate_fio(fio):
    words = fio.split()
    if len(words) == 3:
        return True, None
    elif len(words) == 2:
        return False, "У вас нет отчества?"
    else:
        return False, "Пожалуйста, введите ФИО полностью."

def validate_birth_date(birth_date):
    date_formats = [
        r'\d{1,2}\.\d{1,2}\.\d{4}',
        r'\d{1,2}-\d{1,2}-\d{4}',
        r'\d{1,2} \d{1,2} \d{4}',
        r'\d{1,2}\.\w+\.\d{4}',
        r'\d{1,2}-\w+-\d{4}',
        r'\d{1,2} \w+ \d{4}'
    ]
    for fmt in date_formats:
        if re.match(fmt, birth_date):
            try:
                date = datetime.strptime(birth_date, fmt)
                if date.year > datetime.now().year:
                    return False, "Год рождения не может быть в будущем."
                return True, None
            except ValueError:
                pass
    return False, "Неверный формат даты рождения."

def validate_city(city, branch_cities):
    if city in branch_cities:
        return True, None
    else:
        return False, "В указанном вами городе нет филиала Pedant."

def validate_phone(phone):
    if re.match(r'^\+?\d{1,3}[- ]?\d{1,14}$', phone):
        return True, None
    else:
        return False, "Неверный формат номера телефона."

def validate_email(email):
    if re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        return True, None
    else:
        return False, "Неверный формат email."

async def handle_fio(update, context):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    fio = update.message.text

    is_valid, message = validate_fio(fio)
    if is_valid:
        save_answer(user_id, username, first_name, last_name, 'fio', fio)
        context.user_data['state'] = ApplicationStates.BIRTH_DATE
        await update.message.reply_text("Напишите вашу дату рождения.")
    else:
        await update.message.reply_text(message)

async def handle_birth_date(update, context):
    user_id = update.message.from_user.id
    birth_date = update.message.text

    is_valid, message = validate_birth_date(birth_date)
    if is_valid:
        save_answer(user_id, None, None, None, 'birth_date', birth_date)
        context.user_data['state'] = ApplicationStates.CITY
        await update.message.reply_text("Ваш город проживания?")
    else:
        await update.message.reply_text(message)

async def handle_city(update, context):
    user_id = update.message.from_user.id
    city = update.message.text

    is_valid, message = validate_city(city, context.bot_data['branch_cities'])
    if is_valid:
        save_answer(user_id, None, None, None, 'city', city)
        context.user_data['state'] = ApplicationStates.PHONE
        await update.message.reply_text("Напишите Ваш номер телефона.")
    else:
        await update.message.reply_text(message)

async def handle_phone(update, context):
    user_id = update.message.from_user.id
    phone = update.message.text

    is_valid, message = validate_phone(phone)
    if is_valid:
        save_answer(user_id, None, None, None, 'phone', phone)
        context.user_data['state'] = ApplicationStates.EMAIL
        await update.message.reply_text("Напишите вашу контактную электронную почту.")
    else:
        await update.message.reply_text(message)

async def handle_email(update, context):
    user_id = update.message.from_user.id
    email = update.message.text

    is_valid, message = validate_email(email)
    if is_valid:
        save_answer(user_id, None, None, None, 'email', email)
        context.user_data['state'] = ApplicationStates.COMPLETE
        await update.message.reply_text("Спасибо за заполнение нашей анкеты, ожидайте обратной связи.")
        mark_complete(user_id)
    else:
        await update.message.reply_text(message)