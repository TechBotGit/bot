import telepot
import splinter
import selenium
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
    
    def ParseDateNoColon(self):
        date_no_colon = ''
        for l in self.str_message:
            if l != ':':
                date_no_colon += l
            else:
                continue
        return date_no_colon

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
            a = datetime.datetime(year_week, month_week, day_week+day_plus, hour_start, minute_start)
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
        course_code, location_course, class_type, start_time, end_time, first_recess_week, first_week = self.str_message.split(';')
        self.course_code = course_code
        self.location_course = location_course
        self.class_type = class_type
        self.start_time = start_time
        self.end_time = end_time
        self.first_recess_week = first_recess_week
        self.first_week = first_week


class StringParseIndex(object):
    
    def __init__(self, str_message):
        self.str_message = str_message
        self._course_name = ''
        self._course_type = ''
        self._index = ''
    
    @property
    def course_name(self):
        return self._course_name

    @property
    def course_type(self):
        return self._course_type

    @property
    def index(self):
        return self._index

    @course_name.setter
    def course_name(self, value):
        self._course_name = value
        return self._course_name

    @course_type.setter
    def course_type(self, value):
        self._course_type = value
        return self._course_type

    @index.setter
    def index(self, value):
        self._index = value
        return self._index

    def Parse(self):
        semicolon = []
        for l in self.str_message:
            if l != ';':
                if len(semicolon) == 0:
                    self.course_name += l
                   
                elif len(semicolon) == 1:
                    self.course_type += l
                    
                elif len(semicolon) == 2:
                    self.index += l

            elif l == ' ':
                continue
                
            else:
                semicolon.append(';')
                continue
            
        if len(semicolon) < 2:
            1/0
        self.course_type = self.course_type.lower()
        if self.course_type.find('full') != -1 and self.course_type.find('part') == -1:
            self.course_type = 'F'
        elif self.course_type.find('part') != -1 and self.course_type.find('full') == -1:
            self.course_type = 'P'


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

    def start(self, Course_code, Type_course, index_number):
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
                    soup = BeautifulSoup(html_page, 'html.parser')
                    # print(soup)
                    #ii.close()
        self.parsedatahtml(soup,index_number)
        print('Success')


    def parsedatahtml(self,soup, index_number):
        finish=False
        print(soup)
        tables = soup.find('table',border=True)
        rows = tables.find_all('tr')
        #print(rows)
        for iterator in range (1,len(rows)):
            for columns in range(0,7):
                #print(rows[iterator].find_all('td')[columns])
                self.data[columns].append(rows[iterator].find_all('td')[columns])
                #print (self.data[columns][iterator])
        #print (self.data)
        for iterator in range(len(self.data[columns])):
            if self.data[0][iterator].text==index_number:
                for iterator2 in range(iterator,len(self.data[columns])):
                    if self.data[0][iterator2].text!='' and self.data[0][iterator2].text!=index_number:
                        finish=True
                        break
                    for columns in range(0,7):
                        print(self.data[columns][iterator2].text)
            if finish:
                break
