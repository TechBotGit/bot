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
        self._start_time_cantik = ''
        self._end_time_cantik = ''

        # for STARS Property
        self._course_code = ''
        self._location_course = ''
        self._class_type = ''
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
    def class_type(self):
        return self._class_type
    
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

    @property
    def start_time_cantik(self):
        return self._start_time_cantik

    @property
    def end_time_cantik(self):
        return self._end_time_cantik

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
    
    @class_type.setter
    def class_type(self, value):
        self._class_type = value
        return self._class_type
    
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

    @start_time.setter
    def start_time_cantik(self, value):
        self._start_time_cantik = value
        return self._start_time_cantik

    @end_time.setter
    def end_time_cantik(self, value):
        self._end_time_cantik = value
        return self._end_time_cantik
    
    def ParseEvent(self):
        str_input= self.str_message.split(';')
        if len(str_input)!=4:
            raise ValueError
        for i in range(len(str_input)):
            if i==0:
                self.event_name=str_input[i]

            elif i==1:
                self.location=str_input[i]

            elif i==2:
                self.start_time_cantik = str_input[i]
                print(self.start_time_cantik)
                obj_date = datetime.datetime.strptime(str_input[i], '%Y-%m-%d %H:%M')
                tz = pytz.timezone('Asia/Singapore')
                tz_obj_date = tz.localize(obj_date)
                iso_date = tz_obj_date.isoformat()
                self.start_date = iso_date
            
            elif i==3:
                self.end_time_cantik = str_input[i]
                print(self.end_time_cantik)
                obj_date = datetime.datetime.strptime(str_input[i], '%Y-%m-%d %H:%M')
                tz = pytz.timezone('Asia/Singapore')
                tz_obj_date = tz.localize(obj_date)
                iso_date = tz_obj_date.isoformat()
                self.end_date = iso_date

    def ParseDate(self):
        obj_date = datetime.datetime.strptime(self.str_message, '%Y-%m-%d %H:%M')
        tz = pytz.timezone('Asia/Singapore')
        tz_obj_date = tz.localize(obj_date)
        iso_date = tz_obj_date.isoformat()
        return iso_date

    def ParseDateRange(self):
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
    
    def ParseDateWeek(self, start_week):
        """To exclude any week"""
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
        course_code, location_course, class_type, start_time, end_time = self.str_message.split(';')
        self.course_code = course_code
        self.location_course = location_course
        self.class_type = class_type
        self.start_time = start_time
        self.end_time = end_time


class StringParseIndex(object):
    
    def __init__(self, str_message):
        self.str_message = str_message
        self._course_name = ''
        self._index = ''
    
    @property
    def course_name(self):
        return self._course_name

    @property
    def index(self):
        return self._index

    @course_name.setter
    def course_name(self, value):
        self._course_name = value
        return self._course_name

    @index.setter
    def index(self, value):
        self._index = value
        return self._index

    def Parse(self):
        for l in self.str_message:
            if l == ' ':
                continue
            else:
                self.course_name += l
        

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
            'course_code': [],
            'type': [],
            'group': [],
            'day': [],
            'time': [],
            'venue': [],
            'remark': []
        }

    def selectindex(self,index_number,parsedlist):
        self.data=parsedlist
        finish=False
        #print(soup)
        for iterator in range(len(self.data[0])):
            if self.data[0][iterator].text==index_number:
                for iterator2 in range(iterator,len(self.data[0])):
                    if self.data[0][iterator2].text!='' and self.data[0][iterator2].text!=index_number:
                        finish=True
                        break
                    self.dict["course_code"].append(self.data[0][iterator2].text)
                    self.dict["type"].append(self.data[1][iterator2].text)
                    self.dict["group"].append(self.data[2][iterator2].text)
                    self.dict["day"].append(self.data[3][iterator2].text)
                    self.dict["time"].append(self.data[4][iterator2].text)
                    self.dict["venue"].append(self.data[5][iterator2].text)
                    self.dict["remark"].append(self.data[6][iterator2].text)
                    #for columns in range(0,7):
                        #print(self.data[columns][iterator2].text)
            if finish:
                break
        print(self.dict)     