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
        self.sheet['E1'] = 'index_list'
        
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
    
    def update(self, chat_id, first_week, first_recess_week, student_type=None, index_list=None):
        """Update exisiting workbook"""
        if not self.isChatidExist(chat_id):
            update_list = [chat_id, first_week, first_recess_week, student_type, index_list]
            self.sheet_update.append(update_list)
            self.wb_update.save(self.path_file)
        else:
            print('Updating existing table')
            self.set_table_query(chat_id, first_week, first_recess_week, student_type, index_list)
            self.wb_update.save(self.path_file)
            raise ValueError

    def isChatidExist(self, chat_id):
        for i in range(1, len(self.sheet_update['A'])):
            self.chat_id_list.append(self.sheet_update['A'][i].value)
        return chat_id in self.chat_id_list

    def table_query(self, chat_id, first_week=None, first_recess_week=None, student_type=None, index_list=None):
        """Query table in database \n
        Set the requested data parameter to True to retrieve it. \n
        Returns a list of requested data with the index coresponds to the order of the optional arguments, i.e. first_week has the index 0, first_recess_week has the index 1, etc."""
       
        arg_list = [first_week, first_recess_week, student_type, index_list]
        result_list = []
        for row in self.sheet_update.iter_rows():
            for cell in row:
                if cell.value == chat_id:
                    for i in range(len(arg_list)):
                        if arg_list[i] is not None:
                            result = self.sheet_update.cell(row=cell.row, column=i + 2).value
                            result_list.append(result)
                        else:
                            result_list.append(None)
                    break
                break
        return result_list
    
    def set_table_query(self, chat_id, first_week=None, first_recess_week=None, student_type=None, index_list=None):
        arg_list = [first_week, first_recess_week, student_type, index_list]
        for row in self.sheet_update.iter_rows():
            for cell in row:
                if cell.value == chat_id:
                    for i in range(len(arg_list)):
                        if arg_list[i] is not None:
                            self.sheet_update.cell(row=cell.row, column=i + 2, value=arg_list[i])
                    break
                break
