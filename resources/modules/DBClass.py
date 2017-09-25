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
        self.sheet['E1'] = 'course_code_list'
        
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
    
    def update(self, chat_id, first_week=None, first_recess_week=None, student_type=None, course_code_list=None):
        """Update exisiting workbook"""
        if not self.isChatidExist(chat_id):
            update_list = [chat_id, first_week, first_recess_week, student_type, course_code_list]
            self.sheet_update.append(update_list)
        else:
            print('Updating existing table')
            self.set_table_query(chat_id, first_week, first_recess_week, student_type, course_code_list)

        self.wb_update.save(self.path_file)

    def isChatidExist(self, chat_id):
        for i in range(1, len(self.sheet_update['A'])):
            self.chat_id_list.append(self.sheet_update['A'][i].value)
        return chat_id in self.chat_id_list
    
    def isRecordExist(self, chat_id, first_week=None, first_recess_week=None, student_type=None, course_code_list=None):
        """Description: Check if a particular record exists in the database \n
        Usage: Set the optional parameter to be True to retrieve the data \n
        Return: Boolean
        Note: Only 1 optional parameter can be set to True at a time
        """
        result = None
        for row in self.sheet_update.iter_rows():
            for cell in row:
                if cell.value == chat_id:
                    if first_week:
                        result = self.sheet_update.cell(row=cell.row, column=2).value
                    elif first_recess_week:
                        result = self.sheet_update.cell(row=cell.row, column=3).value
                    elif student_type:
                        result = self.sheet_update.cell(row=cell.row, column=4).value
                    elif course_code_list:
                        result = self.sheet_update.cell(row=cell.row, column=5).value
                    break
        return result is not None
    
    def table_query(self, chat_id, first_week=None, first_recess_week=None, student_type=None, course_code_list=None):
        """Description: Query table in database \n
        Usage: Set the requested data parameter to True to retrieve it. \n
        Return: list \n
        Note: Returns a list of requested data with the index coresponds to the order of the optional arguments, i.e. first_week has the index 0, first_recess_week has the index 1, etc."""
       
        arg_list = [first_week, first_recess_week, student_type, course_code_list]
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
    
    def set_table_query(self, chat_id, first_week=None, first_recess_week=None, student_type=None, course_code_list=None):
        """Description: Query table to set data with the corresponding chat_id \n
        Usage: Set the optional argument to the value that you want to set \n
        Example: set_table_query(<chat_id>, first_week='2017-8-14') \n
        Return: None
        """
        arg_list = [first_week, first_recess_week, student_type, course_code_list]
        for row in self.sheet_update.iter_rows():
            for cell in row:
                if cell.value == chat_id:
                    for i in range(len(arg_list)):
                        if arg_list[i] is not None:
                            self.sheet_update.cell(row=cell.row, column=i + 2, value=arg_list[i])
                    break
                break
