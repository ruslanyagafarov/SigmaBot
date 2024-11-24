# GoogleSheetsService.py
import gspread
import logging
from logger_config import setup_logger

logger = setup_logger()

class GoogleSheetsService:
    def __init__(self, credentials_file, sheet_id):
        self.gc = gspread.service_account(filename=credentials_file)
        self.sheet = self.gc.open_by_key(sheet_id)
        logger.info("GoogleSheetsService initialized")

    def get_branch_cities(self):
        """Возвращает список городов из листа 'филиалы'."""
        logger.info("Retrieving branch cities")
        branch_sheet = self.sheet.worksheet('Филиалы')
        cities = branch_sheet.col_values(1)  # Предполагается, что города находятся в первом столбце
        logger.info(f"Retrieved branch cities: {cities}")
        return cities

    def save_application(self, date, name, city, phone, email):
        """Сохраняет заявку в лист 'заявки'."""
        logger.info(f"Saving application for user {name} from {city}")
        application_sheet = self.sheet.worksheet('Заявки')
        application_sheet.append_row([date, name, city, phone, email])
        logger.info(f"Application saved for user {name} from {city}")