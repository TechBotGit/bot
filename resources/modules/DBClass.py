import pandas as pd
import os
import sys
from openpyxl import load_workbook, Workbook
# from openpyxl.utils.dataframe import dataframe_to_rows


class DB(object):

    def __init__(self):
        """Initialize WorkBook"""
        self.filename = "/../resources/database/database.xlsx"
        self.cwd = os.path.dirname(sys.argv[0])
        self.path_file = self.cwd + self.filename
        self.wb = Workbook()
        self.sheet = self.wb.active
        self.sheet['A1'] = 'chat_id'
        self.sheet['B1'] = 'first_week'
        self.sheet['C1'] = 'first_recess_week'

        self._chat_id_list = []

    @property
    def chat_id_list(self):
        return self._chat_id_list

    @chat_id_list.setter
    def chat_id_list(self, value):
        self._chat_id_list.append(value)
        return self._chat_id_list
    
    def update(self, chat_id, first_week, first_recess_week):
        """Update exisiting workbook"""
        if not os.path.isfile(self.path_file):
            self.wb.save(self.path_file)
        wb_update = load_workbook(self.path_file)
        sheet_update = wb_update.active

        for i in range(1, len(sheet_update['A'])):
            self.chat_id_list.append(sheet_update['A'][i].value)
        if chat_id not in self.chat_id_list:
            update_list = [chat_id, first_week, first_recess_week]
            sheet_update.append(update_list)
            wb_update.save(self.path_file)
        else:
            print('chat_id already exists')
            raise ValueError
