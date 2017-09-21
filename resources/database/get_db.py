import pandas as pd
import os
import sys
from openpyxl import load_workbook, Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

cwd = os.path.dirname(sys.argv[0])
os.chdir(cwd)

filename = "database.xlsx"

wb = load_workbook(filename)
sheet = wb.active

sheet['A1'] = 'user_id'
sheet['B1'] = 'chat_id'
sheet['C1'] = 'event_id'

new_user = 848
new_chat = 134
new_event = 103748952384

update_list = [new_user, new_chat, new_event]

sheet.append(update_list)

wb.save(filename)
