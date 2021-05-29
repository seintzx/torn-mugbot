#!/usr/bin/env python3

import os
import myutils
import gspread
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials


load_dotenv()
WORKBOOK = os.getenv('WORKBOOK')
SHEET_S = os.getenv('SHEET_S')


def auth(worksheet_name):
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'client_secret.json', scope)
    client = gspread.authorize(creds)
    worksheet = client.open(WORKBOOK).worksheet(worksheet_name)
    return worksheet


def update_mug(worksheet_name, log):
    worksheet = auth(worksheet_name)
    rdate = r"[0-9]*/[0-9]*/[0-9]*"
    rcash = r"\$[0-9,]*"

    date = str(myutils.regex(rdate, log))
    cash = convert(myutils.regex(rcash, log))
    new_row = build_row(worksheet, cash, date)

    try:
        # update daily row
        row_number = worksheet.find(date).row
        update_row(worksheet, row_number, cash)
    except:
        # inser new day row
        worksheet.append_row(new_row)
    finally:
        # update total row
        total_row_number = worksheet.find("alltime").row
        update_row(worksheet, total_row_number, cash)


def build_row(worksheet, cash, date):
    # row format: row = [date, success, failed, attack, mugged, profit]
    new_row = []

    new_row.append(date)
    min_cash = get_min()
    if cash <= min_cash:
        new_row.append("0")
        new_row.append("1")
    else:
        new_row.append("1")
        new_row.append("0")

    new_row.append((int(new_row[1]) + int(new_row[2])) * min_cash)
    new_row.append(cash)
    new_row.append(int(new_row[4]) - int(new_row[3]))

    return new_row


def update_row(worksheet, row_number, cash):
    # row format: row = [date, success, failed, attack, mugged, profit]
    old_row = worksheet.row_values(row_number)
    new_row = []

    new_row.append(old_row[0])
    min_cash = get_min()
    if cash <= min_cash:
        new_row.append(old_row[1])
        new_row.append(int(old_row[2]) + 1)
    else:
        new_row.append(int(old_row[1]) + 1)
        new_row.append(old_row[2])
    new_row.append((int(new_row[1]) + int(new_row[2])) * min_cash)
    new_row.append(int(old_row[4]) + cash)
    new_row.append(int(new_row[4]) - int(new_row[3]))

    rang = get_range(row_number, len(new_row))
    worksheet.update(rang, [new_row])


def get_range(row_number, len_new_row):
    r1 = gspread.utils.rowcol_to_a1(row_number,1)
    r2 = gspread.utils.rowcol_to_a1(row_number, len_new_row)
    rang = '{0}:{1}'.format(r1, r2)
    return rang


def get_total_stat(workbook, worksheet_name):
    worksheet = auth(workbook, worksheet_name)
    row_number = worksheet.find("alltime").row
    total_stat = worksheet.row_values(row_number)
    return total_stat


def get_daily_stat(workbook, worksheet_name, date):
    worksheet = auth(workbook, worksheet_name)
    row_number = worksheet.find(date, in_column=1).row
    daily_stat = worksheet.row_values(row_number)
    return daily_stat


def get_min():
    # worksheet = auth(SHEET_S)
    # return convert(worksheet.acell('C7').value)
    return int('1300000')


def convert(value):
    return int(str(value).replace(',','')[1:])


