import datetime
import pytz
import os
import sys

from bs4 import BeautifulSoup
from splinter import Browser


class StringParseGoogleAPI(object):

    """This is a class for string formatting to create google calendar event"""

    def __init__(self, str_message):
        self.str_message = str_message
        self._event_name = ''
        self._location = ''
        self._start_date = ''
        self._end_date = ''

        # for STARS Property
        self._course_code = ''
        self._location_course = ''
        self._course_type = ''
        self._start_time = ''
        self._end_time = ''
        self._first_recess_week = ''
        self._first_week = ''

    @property
    def event_name(self):
        return self._event_name
    
    @property
    def location(self):
        return self._location

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def course_code(self):
        return self._course_code

    @property
    def location_course(self):
        return self._location_course

    @property
    def course_type(self):
        return self._course_type
    
    @property
    def start_time(self):
        return self._start_time

    @property
    def end_time(self):
        return self._end_time

    @property
    def first_recess_week(self):
        return self._first_recess_week

    @property
    def first_week(self):
        return self._first_week

    @event_name.setter
    def event_name(self, value):
        self._event_name = value
        return self._event_name

    @location.setter
    def location(self, value):
        self._location = value
        return self._location

    @start_date.setter
    def start_date(self, value):
        self._start_date = value
        return self._start_date
    
    @end_date.setter
    def end_date(self, value):
        self._end_date = value
        return self._end_date

    @course_code.setter
    def course_code(self, value):
        self._course_code = value
        return self._course_code

    @location_course.setter
    def location_course(self, value):
        self._location_course = value
        return self._location_course
    
    @course_type.setter
    def course_type(self, value):
        self._course_type = value
        return self._course_type
    
    @start_time.setter
    def start_time(self, value):
        self._start_time = value
        return self._start_time

    @end_time.setter
    def end_time(self, value):
        self._end_time = value
        return self._end_time

    @first_recess_week.setter
    def first_recess_week(self, value):
        self._first_recess_week = value
        return self._first_recess_week

    @first_week.setter
    def first_week(self, value):
        self._first_week = value
        return self._first_week
    
    def ParseEvent(self):
        semicolon = []

        for l in self.str_message:
            if l != ';':
                if len(semicolon) == 0:
                    self.event_name += l

                elif len(semicolon) == 1:
                    self.location += l
                
                elif len(semicolon) == 2:
                    self.start_date += l

                elif len(semicolon) == 3:
                    self.end_date += l

            else:
                semicolon.append(';')
                continue

    def ParseDate(self):
        """Description: For freebusy query"""
        obj_date = datetime.datetime.strptime(self.str_message, '%Y-%m-%d %H:%M')
        tz = pytz.timezone('Asia/Singapore')
        tz_obj_date = tz.localize(obj_date)
        iso_date = tz_obj_date.isoformat()
        return iso_date

    def ParseDateRange(self):
        """Description: For isFree command"""
        semicolon = []
        for l in self.str_message:
            if l != ';':
                if len(semicolon) == 0:
                    self.start_date += l
                else:
                    self.end_date += l
            else:
                semicolon.append(';')
                continue
    
    def ParseDateIndex(self, date_string_range):
        """Description: to parse a date range from HTML, e.g. 1430-1530 into 14:30:00 and 15:30:00
        Return: tuple (start, end)
        """
        start_time, end_time = date_string_range.split('-')
        obj_start_time = datetime.datetime.strptime(start_time, '%H%M')
        obj_end_time = datetime.datetime.strptime(end_time, '%H%M')
        str_start_time = obj_start_time.strftime('%H:%M:%S')
        str_end_time = obj_end_time.strftime('%H:%M:%S')
        return str_start_time, str_end_time

    def ParseDateWeek(self, start_week):
        """Description: To exclude any week"""
        hour_start, minute_start, second_start = self.str_message.split(':')
        year_week, month_week, day_week = start_week.split('-')
        
        hour_start = int(hour_start)
        minute_start = int(minute_start)
        second_start = int(second_start)
        year_week = int(year_week)
        month_week = int(month_week)
        day_week = int(day_week)
        
        date_list = []
        date_list_no_colon = []
        date_string_complete = ''

        for day_plus in range(7):
            a = datetime.datetime(year_week, month_week, day_week + day_plus, hour_start, minute_start)
            a = a.isoformat()
            date_list.append(a)

        for item in date_list:
            date_string = ''
            for c in item:
                if c != '-' and c != ':':
                    date_string += c
            date_list_no_colon.append(date_string)

        date_string_complete = ','.join(date_list_no_colon)
        return date_string_complete

    def ParseIndexInput(self):
        course_code, location_course, course_type, start_time, end_time = self.str_message.split(';')
        self.course_code = course_code
        self.location_course = location_course
        self.course_type = course_type
        self.start_time = start_time
        self.end_time = end_time


class StringParseIndex(object):
    
    def __init__(self, str_message):
        self.str_message = str_message
        self._course_code = ''
        self._index = ''
    
    @property
    def course_code(self):
        return self._course_code

    @property
    def index(self):
        return self._index

    @course_code.setter
    def course_code(self, value):
        self._course_code = value
        return self._course_code

    @index.setter
    def index(self, value):
        self._index = value
        return self._index

    def Parse(self):
        for l in self.str_message:
            if l == ' ':
                continue
            else:
                self.course_code += l
        

class StringParseStudentType(object):
    def __init__(self,str_message):
        self.str_message= str_message
        self._course_type= ''
    
    @property
    def course_type(self):
        return self._course_type

    @course_type.setter
    def course_type(self, value):
        self._course_type = value
        return self._course_type

    def ParseInput(self):
        self._course_type = self.str_message.lower()
        if self._course_type.find('full') != -1 and self._course_type.find('part') == -1:
            self._course_type = 'F'
        elif self._course_type.find('part') != -1 and self._course_type.find('full') == -1:
            self._course_type = 'P'
        else:
            raise ValueError


class PreformattedBotInlineMarkup(object):
    """This is a class for storing future fixed KeyboardMarkup"""
    def __init__(self):
        self.days = [
            'Sunday',
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday'
        ]


class splintergetdata(object):
    def __init__(self):
        self.url = "https://wish.wis.ntu.edu.sg/webexe/owa/aus_schedule.main"
        self.cwd = os.path.dirname(sys.argv[0])
        self.browser_file = self.cwd + "/../resources/browser.txt"
        f = open(self.browser_file, 'r')
        self.browser_used = f.read()
        f.close()
        self.data=[[],[],[],[],[],[],[]]
        self.indexlist=[]
        self.soup = ''
        #only for initialization, duck typing will change its format later XD

    def start(self, Course_code, Type_course):
        with Browser(self.browser_used) as browser:
            browser.visit(self.url)
            browser.fill("r_subj_code", Course_code)
            browser.choose("r_search_type", Type_course)
            browser.find_by_value("Search").first.click()
            #while len(browser.windows)>0:
            for ii in browser.windows:
                if ii.url == "https://wish.wis.ntu.edu.sg/webexe/owa/AUS_SCHEDULE.main_display1":
                    browser.windows.current = ii
                    html_page = browser.html
                    # print(html_page)
                    self.soup = BeautifulSoup(html_page, 'html.parser')
                    #had to declare soup self here :'(
                    # print(soup)
                    #ii.close()
        print('Success')

    def parsedatahml(self):
        tables = self.soup.find('table',border=True)
        rows = tables.find_all('tr')
        #print(rows)
        for iterator in range (1,len(rows)):
            for columns in range(0,7):
                #print(rows[iterator].find_all('td')[columns])
                self.data[columns].append(rows[iterator].find_all('td')[columns])
                #print (self.data[columns][iterator])
            if self.data[0][-1].text!='':
                    self.indexlist.append(self.data[0][-1].text)
        #print(self.indexlist)
        #print (self.data)
        #print(type(self.data))
        return self.data


class chooseindex(object):
    def __init__(self):
        self.data=[[],[],[],[],[],[],[]]
        self.dict = {
            'course_index': [],
            'course_type': [],
            'course_group': [],
            'day': [],
            'time': [],
            'location': [],
            'recurrence': []
        }

    def selectindex(self,index_number,parsedlist):
        self.data=parsedlist
        finish=False
        for iterator in range(len(self.data[0])):
            if self.data[0][iterator].text==index_number:
                for iterator2 in range(iterator,len(self.data[0])):
                    if self.data[0][iterator2].text!='' and self.data[0][iterator2].text!=index_number:
                        finish=True
                        break
                    self.dict["course_index"].append(self.data[0][iterator2].text)
                    self.dict["course_type"].append(self.data[1][iterator2].text)
                    self.dict["course_group"].append(self.data[2][iterator2].text)
                    self.dict["day"].append(self.data[3][iterator2].text)
                    self.dict["time"].append(self.data[4][iterator2].text)
                    self.dict["location"].append(self.data[5][iterator2].text)
                    self.dict["recurrence"].append(self.data[6][iterator2].text)

            if finish:
                break
        return self.dict
