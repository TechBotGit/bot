class StringParse(object):
    """This is a class for string formatting to create google calendar event"""

    def __init__(self, str_message):
        self.str_message = str_message
        self.event_name = ''
        self.location = ''
        self.start_date = ''
        self.end_date = ''
   
    def Parse(self):
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
