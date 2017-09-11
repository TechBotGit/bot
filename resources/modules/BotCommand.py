import sys
import os


class API (object):
    def __init__(self):
        self.cwd = os.path.dirname(sys.argv[0])
        self.api_key = self.cwd + '/a.txt'
        f = open(self.api_key, 'r')
        self.token = f.read()
        f.close()


class BotCommand(API):

    def __init__(self, command):
        API.__init__(self)
        self.command = command
        self.command_list = [
            '/start',
            '/createevent',
            '/mergeevent',
            '/quit'
        ]

    def isValidCommand(self, command):
        return command in self.command_list

    def executeCommand(self, command):
        if self.isValidCommand(command):
            if command == '/start':
                return "Beep. You can start chatting with me now, or ask me to do stuff. :)"
            else:
                return "Command not updated"
        else:
            return "Command valid!"
