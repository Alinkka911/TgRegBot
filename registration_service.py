from spreadsheet import SpreadsheetManager

KEY_FILE_LOCATION = 'tg-bot-421112-4814e071cafa.json'
SHEET_ID = "12rKgsq0zUmgP2lykXcpry9KuUmmTzj18qRGYE_pjdbM"
max_team_size = 10


class RegistrationService:
    def __init__(self):
        self.spreadsheet_manager = SpreadsheetManager(KEY_FILE_LOCATION, SHEET_ID)

    def get_available_dates(self):
        dates_data = self.spreadsheet_manager.get_all_records()
        return [row["Date"] for row in dates_data if row.get("DateInfo", "").lower() != "full"]

    def register_team(self, team_data):
        # Extract data from team_data dictionary
        date, user_id, user_name, team_name, team_size, leader_name, phone_number = team_data.values()

        # Get the worksheet for the selected date
        worksheet = self.spreadsheet_manager.get_worksheet(date)

        # Append the new row with team information
        new_row = [user_id, user_name, team_name, team_size, leader_name, phone_number]
        worksheet.append_row(new_row)

        # Check if the sheet is full and update the main sheet if needed
        if len(worksheet.get_all_records()) == max_team_size:
            self.spreadsheet_manager.update_date_status(date, "full")

    def is_user_registered(self, user_id):
        for sheet_name in self.spreadsheet_manager.get_sheet_names():
            worksheet = self.spreadsheet_manager.get_worksheet(sheet_name)
            cell = worksheet.find(str(user_id))
            if cell:
                return True
        return False

    def get_user_registration_data(self, user_id):
        for sheet_name in self.spreadsheet_manager.get_sheet_names():
            worksheet = self.spreadsheet_manager.get_worksheet(sheet_name)
            cell = worksheet.find(str(user_id))
            if cell:
                row_data = worksheet.row_values(cell.row)
                # Adjust data extraction based on your sheet structure
                return {
                    "date": sheet_name,
                    "user_id": row_data[0],
                    "user_name": row_data[1],
                    "team_name": row_data[2],
                    "team_size": row_data[3],
                    "leader_name": row_data[4],
                    "phone_number": row_data[5]
                }
        return None  # Return None if user not found

    def get_registered_teams_for_date(self, date):
        worksheet = self.spreadsheet_manager.get_worksheet(date)
        return worksheet.get_all_records()

    def get_time_and_address(self, date):
        worksheet = self.spreadsheet_manager.get_worksheet("Sheet1")
        return worksheet.cell(worksheet.find(date).row, worksheet.find("Time&Address").col).value
