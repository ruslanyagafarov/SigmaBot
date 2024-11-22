import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

class NotificationService:
    def __init__(self):
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.starttls()
        self.server.login('', '')

    def send_email_to_branch(self, city, name):
        # Убираем пробелы и приводим к нижнему регистру
        recipient_email = f"branch_{city.lower().strip()}@example.com"

        message = MIMEMultipart()
        message['From'] = 'your_email@gmail.com'
        message['To'] = recipient_email
        message['Subject'] = 'New Application'

        body = f'New application: {name} from {city}.'
        message.attach(MIMEText(body, 'plain'))

        try:
            self.server.sendmail('your_email@gmail.com', recipient_email, message.as_string())
            print("Email successfully sent!")
        except Exception as e:
            print(f"Ошибка при отправке письма: {e}")

    def close(self):
        self.server.quit()
