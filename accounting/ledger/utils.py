"""Utilities for Accounting ledger app"""

import xlrd
import re
from datetime import datetime


def get_ledger_info(file: str) -> dict:
    """Reads an excel sheet and returns a dictionary of account ledger information"""

    ledger_info = {}
    wb = xlrd.open_workbook(file)
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)

    dates = re.findall(r'\d{2}\.\d{2}\.\d{4}', sheet.cell(2, 0).value)

    ledger_info['bank'] = sheet.cell_value(0, 0)
    ledger_info['description'] = " ".join([sheet.cell_value(1, 0), sheet.cell_value(2, 0), sheet.cell_value(3, 0)])
    ledger_info['compiled_at'] = xlrd.xldate_as_datetime(sheet.cell(5, 0).value, 0)
    ledger_info['start_period'] = datetime.strptime(dates[0], '%d.%m.%Y').date()
    ledger_info['end_period'] = datetime.strptime(dates[1], '%d.%m.%Y').date()
    ledger_info['classes'] = {}

    for row in range(8, sheet.nrows):
        if sheet.cell_type(row, 1) == 0:
            account_class = re.compile(r'^КЛАСС  \d  (.*)$').search(sheet.cell(row, 0).value).group(1)
            class_number = re.search(r'\d', sheet.cell(row, 0).value).group(0)
            ledger_info['classes'][class_number] = account_class

    return ledger_info


def read_excel(file: str) -> list:
    """Reads an excel sheet and returns a list of accounts"""

    accounts = []
    account = []
    wb = xlrd.open_workbook(file)
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)

    for row in range(9, sheet.nrows):
        for col in range(sheet.ncols):
            if sheet.cell(row, col).value:
                account.append(sheet.cell(row, col).value)

        accounts.append(account)
        account = []

    for account in accounts:
        print(account)

    return accounts
