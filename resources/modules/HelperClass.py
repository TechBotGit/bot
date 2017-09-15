import datetime
import pytz


class StringParse(object):
    """This is a class for string formatting to create google calendar event"""

    def __init__(self, str_message):
        self.str_message = str_message
        self.event_name = ''
        self.location = ''
        self.start_date = ''
        self.end_date = ''

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
