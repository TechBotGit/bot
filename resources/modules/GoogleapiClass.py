from __future__ import print_function
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import httplib2
import os
import HelperClass as hc
import datetime
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

except ImportError:
    flags = None


class GoogleAPI(object):

    def __init__(self):
        # If modifying these SCOPES, delete your previously saved credentials
        # at ~/.credentials/calendar-python-quickstart.json
        self.SCOPES = 'https://www.googleapis.com/auth/calendar'
        self.CLIENT_SECRET_FILE = '../api/client_secret.json'
        self.APPLICATION_NAME = 'Google Calendar API Python Quickstart'
        self.credentials = self.get_credentials()
        self.http = self.credentials.authorize(httplib2.Http())
        self.service = discovery.build('calendar', 'v3', http=self.http)

    def get_credentials(self):
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        
        credential_path = os.path.join(credential_dir, 'calendar-python-quickstart.json')
        store = Storage(credential_path)
        credentials = store.get()
        
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            
            else:  # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            
            print('Storing credentials to ' + credential_path)
        
        return credentials

    def createEvent(self, summary, location, start, end):

        # Event Details
        event = {
            'summary': summary,
            'location': location,
            'description': 'Created by TechBot',
            'start': {
                'dateTime': start,
                'timeZone': 'Asia/Singapore',
            },
            'end': {
                'dateTime': end,
                'timeZone': 'Asia/Singapore',
            },
            'attendees': [
                {'email': 'jasoncobalagi@gmail.com'}
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 60}
                ],
            },
        }
        event = self.service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))
        return event.get('id')

    def CreateEventIndex(self, summary, location, desc, start_time, end_time, first_week, first_recess_week, recurrence, day, is_ignore_first_event=False):

        first_event_str_start = first_week + start_time
        first_event_obj_start = datetime.datetime.strptime(first_event_str_start, '%Y-%m-%d%H:%M:%S')
        first_event_iso_start = first_event_obj_start.isoformat()
        first_event_ugly_start = first_event_obj_start.strftime("%Y%m%dT%H%M%S")
        
        first_event_str_end = first_week + end_time
        first_event_obj_end = datetime.datetime.strptime(first_event_str_end, '%Y-%m-%d%H:%M:%S')
        first_event_iso_end = first_event_obj_end.isoformat()
        
        # Ignore any particular week
        ParseObject = hc.StringParseGoogleAPI(start_time)
        ParseObject.ParseDateWeek(first_week)
        ignore_first_week = ParseObject.date_string_complete
        
        ParseObject.ParseDateWeek(first_recess_week)
        ignore_recess_week = ParseObject.date_string_complete

        # ignore the first event
        ignore_first_event = ""
        # Comma Issues
        if is_ignore_first_event:
            if recurrence != '':
                ignore_first_event = ',' + first_event_ugly_start + ','
            else:
                ignore_first_event = ',' + first_event_ugly_start
        else:
            recurrence = ',' + recurrence
        # Event Details
        event = {
            'summary': summary,
            'location': location,
            'description': desc,
            'start': {
                'dateTime': first_event_iso_start,
                'timeZone': 'Asia/Singapore',
            },
            'end': {
                'dateTime': first_event_iso_end,
                'timeZone': 'Asia/Singapore',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 60}
                ],
            },
            'recurrence': [
                "EXDATE;TZID=Asia/Singapore;VALUE=DATE:" + ignore_recess_week + ignore_first_event + recurrence,
                # "RDATE;TZID=Asia/Singapore;VALUE=DATE:20170609T100000,20170611T100000",
                "RRULE:FREQ=WEEKLY;UNTIL=20171118;BYDAY=" + day
            ]
        }

        event = self.service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))
   
    def FreeBusyQuery(self, str_date_start, str_date_end):  # str_date --> yyyy-mm-dd hh:mm
        
        # Parsing date
        iso_date_start = hc.StringParseGoogleAPI(str_date_start).ParseDate()
        iso_date_end = hc.StringParseGoogleAPI(str_date_end).ParseDate()

        # query details
        query = {
            'timeMin': iso_date_start,
            'timeMax': iso_date_end,
            'timeZone': 'Asia/Singapore',
            'items': [
                {
                    'id': 'primary'
                }
            ]
        }
        query = self.service.freebusy().query(body=query).execute()
        return query

    def isFree(self, query):
        return len(query['calendars']['primary']['busy']) == 0
   
    def BusyInfo(self, query):
        busy = query['calendars']['primary']['busy']
        start_busy = busy[0]['start']
        end_busy = busy[0]['end']
        return start_busy, end_busy

    def deleteEvent(self,InputtedeventID):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
        service.events().delete(calendarId='primary', eventId=InputtedeventID).execute()
