from __future__ import print_function
import httplib2
import os
import sys

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

sys.path.append('../resources/modules')
from HelperClass import StringParseGoogleAPI

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = '../resources/api/client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def createEvent(summary, location, desc, start_time, end_time):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    
    first_week_date = "2017-08-14"
    
    # Splitting strings
    hour_start, min_start, sec_start = start_time.split(':')
    year_fw, month_fw, day_fw = first_week_date.split('-')
    
    # Combining strings
    first_date = year_fw + month_fw + day_fw
    first_time = hour_start + min_start + sec_start
    first_event = first_date + 'T' + first_time

    # Ignore any particular week
    recess_week = StringParseGoogleAPI(start_time).ParseDateWeek('2017-10-2')
    first_week = StringParseGoogleAPI(start_time).ParseDateWeek()
    
    # Event Details
    event = {
        'summary': summary,
        'location': location,
        'description': desc,
        'start': {
            'dateTime': first_week_date + "T" + start_time,
            'timeZone': 'Asia/Singapore',
        },
        'end': {
            'dateTime': first_week_date + "T" + end_time,
            'timeZone': 'Asia/Singapore',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 60}
            ],
        },
        'recurrence': [
            "EXDATE;TZID=Asia/Singapore;VALUE=DATE:" + recess_week,
            # "RDATE;TZID=Asia/Singapore;VALUE=DATE:20170609T100000,20170611T100000",
            "RRULE:FREQ=WEEKLY;COUNT=7;BYDAY=MO;INTERVAL=2"
        ]
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))


if __name__ == '__main__':
    createEvent('CZ1005', 'HWLAB3', 'LABORATORY', '14:30:00', '16:30:00')
