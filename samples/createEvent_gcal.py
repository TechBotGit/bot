from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

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


def createEvent():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    # Event Details
    event = {
        'summary': 'Meeting Bot Recursive',
        'location': 'Nanyang Technological University',
        'description': 'Let us be a TechBot',
        'start': {
            'dateTime': '2017-06-01T10:00:00',
            'timeZone': 'Asia/Singapore',
        },
        'end': {
            'dateTime': '2017-06-01T14:00:00',
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
        'recurrence': [
            "EXDATE;TZID=Asia/Singapore;VALUE=DATE:20170610T100000",
            "RDATE;TZID=Asia/Singapore;VALUE=DATE:20170609T100000,20170611T100000",
            "RRULE:FREQ=DAILY;UNTIL=20170628;INTERVAL=3"
        ]
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))


if __name__ == '__main__':
    createEvent()
