import pandas as pd
import os
import sys
from openpyxl import load_workbook, Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.utils import get_column_letter, column_index_from_string

cwd = os.path.dirname(sys.argv[0])
os.chdir(cwd)

filename = "database.xlsx"

wb = load_workbook(filename)
sheet = wb.active
chat_id_test = 200158786
print("iter_cols()")
for col in sheet.iter_cols():
    for cell in col:
        print(cell.value)

print('---------------')
print("iter_rows()")
for row in sheet.iter_rows():
    for cell in row:
        if cell.value == chat_id_test:
            print(cell.row)
            sheet.cell(row=cell.row, column=4, value='FullTime')
            break

wb.save(filename)
