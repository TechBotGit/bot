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
        self.sheet['D1'] = 'student_type'
        
        # If file doesn't exist, create it
        if not os.path.isfile(self.path_file):
            self.wb.save(self.path_file)
        
        # for updating method
        self.wb_update = load_workbook(self.path_file)
        self.sheet_update = self.wb_update.active

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
        if not self.isChatidExist(chat_id):
            update_list = [chat_id, first_week, first_recess_week]
            self.sheet_update.append(update_list)
            self.wb_update.save(self.path_file)
        else:
            print('chat_id already exists')
            raise ValueError

    def isChatidExist(self, chat_id):
        for i in range(1, len(self.sheet_update['A'])):
            self.chat_id_list.append(self.sheet_update['A'][i].value)
        return chat_id in self.chat_id_list
    
    def table_query(self, chat_id, first_week=None, first_recess_week=None):
        """Query table in database
            set first_week to True to get the first_week
            set first_recess_week to True to get the first_recess_week
            Either first_week or first_recess_week must be True
        """
        for row in self.sheet_update.iter_rows():
            for cell in row:
                if cell.value == chat_id:
                    if first_week and not first_recess_week:
                        result = self.sheet_update.cell(row=cell.row, column=2).value
                    elif first_recess_week and not first_week:
                        result = self.sheet_update.cell(row=cell.row, column=3).value
                    else:
                        print('Must set first_week or first_recess_week to True')
                        raise ValueError
                        break
                    break
        return result
