import gspread
from oauth2client.service_account import ServiceAccountCredentials




class SpreadsheetManager:
    def __init__(self, key_file_location, sheet_id):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(key_file_location, scope)
        self.gc = gspread.authorize(creds)
        self.sheet = self.gc.open_by_key(sheet_id)

    def get_all_records(self):
        return self.sheet.sheet1.get_all_records()

    def get_worksheet(self, sheet_name):
        return self.sheet.worksheet(sheet_name)

    def get_sheet_names(self):
        return [worksheet.title for worksheet in self.sheet.worksheets()]

    def update_date_status(self, date, status):
        worksheet = self.sheet.sheet1
        date_cell = worksheet.find(date)
        worksheet.update_cell(date_cell.row, 2, status)