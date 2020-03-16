from oauth2client.service_account import ServiceAccountCredentials
import gspread
import csv
import os


def save_last_updated_date(date):
    cwd = os.getcwd()
    cwd = cwd + "/data/last_updated_date.csv"

    with open(cwd, "w") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([date])


def get_last_updated_date():
    updated_date = None
    cwd = os.getcwd()
    cwd = cwd + "/data/last_updated_date.csv"

    with open(cwd, "r") as csvfile:
        csvreader = csv.reader(csvfile)
        for data in csvreader:
            updated_date = data

    return updated_date[0]


class GoogleSheetConnector:

    def __init__(self, spreadsheet_key):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('/data/prod-stage3-48d352795000070.json', scope)
        client = gspread.authorize(creds)
        book = client.open_by_key(spreadsheet_key)
        self.worksheet = book.worksheet("Sheet1")

    def update_sheet(self, data, alphabet, isDict=0, isKey=0):

        length_sku = len(data) + 3

        cell_list = self.worksheet.range(f"{alphabet}3:{alphabet}{length_sku}")

        if isDict:
            if isKey:
                for idx, key_value in enumerate(sorted(data.items(), key=lambda item: item[1], reverse=True)):
                    cell_list[idx].value = key_value[0]
            else:
                for idx, key_value in enumerate(sorted(data.items(), key=lambda item: item[1], reverse=True)):
                    cell_list[idx].value = key_value[1]
        else:
            for idx, data2 in enumerate(data):
                cell_list[idx].value = data2

        self.worksheet.update_cells(cell_list)

    def clear_sheet(self):
        # Clearing the sheet's previous data
        self.worksheet.resize(rows=1)
        self.worksheet.resize(rows=5000)

        # Clearing the header
        range_of_cells = self.worksheet.range('A1:CC1')
        for cell in range_of_cells:
            cell.value = ''
        self.worksheet.update_cells(range_of_cells)

    def add_header(self, user):
        lst = list()
        cwd = os.getcwd()

        if user == "merch":
            cwd = cwd + "/data/merchandising_header_names.csv"
        elif user == "mark":
            cwd = cwd + "/data/marketing_header_names.csv"

        with open(cwd, "r") as csvfile:
            csvreader = csv.reader(csvfile)
            for data in csvreader:
                lst = data

        for data in enumerate(lst):
            self.worksheet.update_cell(1, data[0] + 1, data[1])

