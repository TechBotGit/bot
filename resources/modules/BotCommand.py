class BotCommand(object):

    def __init__(self, command):
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
