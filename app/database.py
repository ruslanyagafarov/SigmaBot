import json
import os
from datetime import datetime

DATABASE_FILE = 'applications.json'

def load_database():
    if not os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'w') as f:
            json.dump([], f)
    with open(DATABASE_FILE, 'r') as f:
        return json.load(f)

def save_database(data):
    with open(DATABASE_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def save_answer(user_id, username, first_name, last_name, question, answer, is_valid=True):
    data = load_database()
    entry = next((item for item in data if item['user_id'] == user_id), None)
    if entry:
        entry[question] = answer
        entry['is_valid'] = is_valid
    else:
        data.append({
            'user_id': user_id,
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'fio': None,
            'birth_date': None,
            'city': None,
            'phone': None,
            'email': None,
            'submission_time': datetime.now().isoformat(),
            'is_complete': False,
            'is_valid': is_valid,
            question: answer
        })
    save_database(data)

def mark_complete(user_id):
    data = load_database()
    entry = next((item for item in data if item['user_id'] == user_id), None)
    if entry:
        entry['is_complete'] = True
    save_database(data)