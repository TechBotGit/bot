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
        self._course_type = ''
        self._start_time = ''
        self._end_time = ''
        self._first_recess_week = ''
        self._first_week = ''

        # For recurrence property
        self._day = []
        self.occuring_week = []
        self.ignored_week = []
        self.format_day = {
            'MON': 'MO',
            'TUE': 'TU',
            'WED': 'WE',
            'THU': 'TH',
            'FRI': 'FR',
            'SAT': 'SA'
        }
        self.date_string_complete = ' '

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
    
    @property
    def day(self):
        return self._day

    # @property
    # def occuring_week(self):
    #     return self._occuring_week

    # @property
    # def ignored_week(self):
    #     return self._ignored_week

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
    
    @day.setter
    def day(self, value):
        self._day = self.format_day[value]

    @start_time_cantik.setter
    def start_time_cantik(self, value):
        self._start_time_cantik = value
        return self._start_time_cantik

    @end_time_cantik.setter
    def end_time_cantik(self, value):
        self._end_time_cantik = value
        return self._end_time_cantik

    # @occuring_week.setter
    # def occuring_week(self, value):
    #     self._occuring_week.append(value)
    #     return self._occuring_week

    # @ignored_week.setter
    # def ignored_week(self, value):
    #     self._ignored_week = value
    #     return self._ignored_week

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
        # date_string_complete = ''

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

        self.date_string_complete = ','.join(date_list_no_colon)

    def ParseIndexInput(self):
        course_code, location_course, course_type, start_time, end_time = self.str_message.split(';')
        self.course_code = course_code
        self.location_course = location_course
        self.course_type = course_type
        self.start_time = start_time
        self.end_time = end_time
    
    def week_range(self, string, lst):
        start, end = string.split('-')
        start = int(start)
        end = int(end)
        for i in range(start, end + 1):
            lst.append(i)
    
    def ParseOccurIgnoreWeek(self, start_week, start_time):
        query_recur = self.str_message
        start = 1
        end = 13
        date_list = []
        date_list_no_colon = []
        helper_list = []
        if query_recur != '':
            query_recur = query_recur.replace('Wk', '')
            if query_recur.count('-') == 0:
                # Separate the delimiter
                self.occuring_week = query_recur.split(',')

                # Convert everything to integer
                self.occuring_week = list(map(int, self.occuring_week))

            else:
                if query_recur.count(',') == 0:
                    self.week_range(query_recur, self.occuring_week)
                else:
                    helper_list = query_recur.split(',')
                    for i in range(len(helper_list)):
                        if helper_list[i].count('-') == 0:  # NO DASH
                            self.occuring_week.append(int(helper_list[i]))
                        else:
                            self.week_range(helper_list[i], self.occuring_week)
        else:
            for i in range(start, end + 1):
                self.occuring_week.append(i)

        self.ignored_week = [x for x in range(1, 14) if x not in self.occuring_week]
        for free_week in self.ignored_week:
            if free_week > 7:
                free_week += 1
            start_week_obj = datetime.datetime.strptime(start_week + start_time, '%Y-%m-%d%H:%M:%S') + datetime.timedelta(days=7 * (free_week - 1))
            for day_plus in range(7):
                increment_day = start_week_obj + datetime.timedelta(days=day_plus)
                increment_day = increment_day.isoformat()
                date_list.append(increment_day)

        for item in date_list:
            date_string = ''
            for c in item:
                if c != '-' and c != ':':
                    date_string += c
            date_list_no_colon.append(date_string)

        self.date_string_complete = ','.join(date_list_no_colon)


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

    def start(self, Course_code, Type_course):
        with Browser(self.browser_used) as browser:
            browser.visit(self.url)
            browser.fill("r_subj_code", Course_code)
            browser.choose("r_search_type", Type_course)
            browser.find_by_value("Search").first.click()
            # while len(browser.windows)>0:
            for ii in browser.windows:
                if ii.url == "https://wish.wis.ntu.edu.sg/webexe/owa/AUS_SCHEDULE.main_display1":
                    browser.windows.current = ii
                    html_page = browser.html
                    # print(html_page)
                    self.soup = BeautifulSoup(html_page, 'html.parser')
        print('Success')

    def parsedatahml(self):
        tables = self.soup.find('table',border=True)
        rows = tables.find_all('tr')
        # print(rows)
        for iterator in range(1,len(rows)):
            for columns in range(0,7):
                # print(rows[iterator].find_all('td')[columns])
                self.data[columns].append(rows[iterator].find_all('td')[columns])
                # print (self.data[columns][iterator])
            if self.data[0][-1].text!='':
                    self.indexlist.append(self.data[0][-1].text)
        # print(self.indexlist)
        # print (self.data)
        # print(type(self.data))
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
