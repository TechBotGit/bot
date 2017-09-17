import telepot
import splinter
import selenium
import datetime
import pytz

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


class PreformattedBotInlineMarkup():
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


class splintergetdata():
    def __init__(self):
        self.url = "https://wish.wis.ntu.edu.sg/webexe/owa/aus_schedule.main"
        # if necessary
    
    def start(self, Course_code, Type_course, index_number):
        with Browser() as browser:
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
                    soup = BeautifulSoup(html_page, 'html.parser')
                    # print(soup)
                ii.close()
        print('Success')
