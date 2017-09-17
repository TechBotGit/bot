from __future__ import print_function
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import httplib2
import os
import datetime
import HelperClass as hc

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
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        # Event Details
        event = {
            'summary': summary,
            'location': location,
            'description': 'Let us be a TechBot',
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

        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))
    
    def FreeBusyQuery(self, str_date_start, str_date_end):  # str_date --> yyyy-mm-dd hh:mm
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
        
        # Parsing date
        iso_date_start = hc.StringParse(str_date_start).ParseDate()
        iso_date_end = hc.StringParse(str_date_end).ParseDate()

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
        query = service.freebusy().query(body=query).execute()
        return query

    def isFree(self, query):
        return len(query['calendars']['primary']['busy']) == 0
   
    def BusyInfo(self, query):
        busy = query['calendars']['primary']['busy']
        start_busy = busy[0]['start']
        end_busy = busy[0]['end']
        return start_busy, end_busy
