import gspread

class GoogleSheetsService:
    def __init__(self, credentials_file, sheet_id):
        self.gc = gspread.service_account(filename=credentials_file)
        self.sheet = self.gc.open_by_key(sheet_id)

    def get_branch_cities(self):
        """Возвращает список городов из листа 'филиалы'."""
        branch_sheet = self.sheet.worksheet('Филиалы')
        return branch_sheet.col_values(1)  # Предполагается, что города находятся в первом столбце

    def save_application(self, date, name, city, phone, email):
        """Сохраняет заявку в лист 'заявки'."""
        application_sheet = self.sheet.worksheet('Заявки')
        application_sheet.append_row([date, name, city, phone, email])
