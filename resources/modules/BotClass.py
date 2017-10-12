import json
import telepot
import datetime
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Custom Class
import GoogleapiClass as gc
import HelperClass as hc
import DBClass as db
import ErrorClass as err


class API(object):
    """API Basic initialisation"""
    def __init__(self):
        # Deploy Bot
        self.api_key = '../resources/token.txt'
        f = open(self.api_key, 'r')
        self.token = f.read()
        f.close()
        self.bot = telepot.Bot(self.token)
        
        # Important storage information
        self._db_chat = {}
        self._list_update_message = []
        
        # additional information for course codes and indexes
        self._indexchosen = ''
        self._parseddataindex = [[],[],[],[],[],[],[]]

        # Error raising
        self._error = 0

        # Static message
        self.suggestion = "What you probably want to do next: "
        self.successRecordDatabase = 'Sucessfull! Your data has been recorded in our database!'
        self.successRecordDatabaseandCalendar = 'Sucessfull! You data has been recorded in our database and your Google Calendar!'

        self.successRemoveDatabase = 'Your data has been removed from our database!'
        self.successRemoveDatabaseandCalendar = 'Your data has been removed from our database and your Google Calendar!'

        self.failRecordDatabase = 'Your data is not recorded in our database!'
        self.failRecordDatabaseandCalendar = 'Your data is not recorded in our database and your Google Calendar!'

        self.failRemoveDatabase = 'Your data is not removed from our database!'
        self.failRemoveDatabaseandCalendar = 'Your data is not removed from our database and your Google Calendar!'

        # Help message
        self.helpMessage = "*Basic Commands* \n"
        self.helpMessage += "/start - Send welcome message \n"
        self.helpMessage += "/help - list available commands \n"
        self.helpMessage += "/quit - Send good bye message \n\n"

        self.helpMessage += "*General Commands* \n"
        self.helpMessage += "/isfree - To check whether you are free at a certain time interval \n"
        self.helpMessage += "/getupcomingevent - List your upcoming events \n\n"

        self.helpMessage += "*Event-related Commands* \n"
        self.helpMessage += "/addevent - Add an event to your Google Calendar \n"
        self.helpMessage += "/removeevent - Remove an event from your Google Calendar \n"
        self.helpMessage += "/getevent - List all events that you have added \n\n"

        self.helpMessage += "*Course-related Commands* \n"
        self.helpMessage += "/addcourse - Add a course schedule to your Google Calendar \n"
        self.helpMessage += "/removecourse - Remove a course schedule from your Google Calendar \n"
        self.helpMessage += "/getcourse - List all courses that you have added \n"
        self.helpMessage += "/setstudenttype - Set your student type (Full Time or Part Time) \n"
        self.helpMessage += "/addfirstweek - Add the first weekday, i.e. Monday, of your first week and recess week \n"
        
    @property
    def db_chat(self):
        return self._db_chat

    @property
    def list_update_message(self):
        return self._list_update_message

    @property
    def indexchosen(self):
        return self._indexchosen
    
    @property
    def parseddataindex(self):
        return self._parseddataindex
    
    @property
    def error(self):
        return self._error
    
    @db_chat.setter
    def db_chat(self, value):
        self._db_chat = value

    @list_update_message.setter
    def list_update_message(self, value):
        self._list_update_message = value

    @indexchosen.setter
    def indexchosen(self, value):
        self._indexchosen = value

    @parseddataindex.setter
    def parseddataindex(self, value):
        self._parseddataindex = value

    @error.setter
    def error(self, value):
        self._error = value
        return self._error

    def handleAPI(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        print(content_type, chat_type, chat_id)
        response = self.bot.getUpdates()
        try:
            self.StoreChat(response)
        except: 
            self.bot.sendMessage(chat_id,"Please write slowly!")
            raise err.ParseError("Typed too fast!")
        # self.StoreChat(response)

        if content_type == 'text':

            # Convert the message to lower case
            msg_received = msg['text'].lower()

            # If the message is a valid command
            if BotCommand(msg_received).isValidCommand():
                # Send users a message related to the command
                if msg_received == '/start':
                    self.bot.sendMessage(chat_id, "Hi, %s! Need help to be more productive? Good news, I'm here to manage your time! Feel free to ask me stuff!" %(msg['chat']['first_name']))
                    self.bot.sendMessage(chat_id, "*Want to know me more?* Just ask me whatever you want and hope I can understand", parse_mode='Markdown')
                    self.bot.sendMessage(chat_id, "*Want to know what I can do?* Just run /help to see commands that I can do to help you", parse_mode='Markdown')
                
                elif msg_received == '/help':
                    self.bot.sendMessage(chat_id, "Here is the list of commands that I can do: ")
                    self.bot.sendMessage(chat_id, self.helpMessage, parse_mode="Markdown")

                elif msg_received == '/addevent':
                    msg_reply = "Okay send me the details in following format:"
                    str_format = "*Event Name;location;YYYY-MM-DD HH:MM;YYYY-MM-DD HH:MM*"
                    self.bot.sendMessage(chat_id, msg_reply)
                    self.bot.sendMessage(chat_id, str_format, parse_mode="Markdown")
                    self.bot.sendMessage(chat_id, "*For example:*", parse_mode="Markdown")
                    self.bot.sendMessage(chat_id, "_Party;NTU;2017-10-08 20:00;2017-10-08 22:00_", parse_mode="Markdown")
                    print(response)
                
                elif msg_received == '/removeevent':
                    excel = db.DB()
                    course_code_str = excel.table_query(chat_id, other_event_id=True)[4]
                    
                    if not excel.isRecordExist(chat_id, other_event_id=True) or course_code_str is None:
                        self.bot.sendMessage(chat_id,"There is nothing to remove...")
                        self.bot.sendMessage(chat_id, self.suggestion)
                        self.bot.sendMessage(chat_id, "Run /addevent to add an event")
                    else:
                        course_code_dict = json.loads(course_code_str)
                        evt_name_list = [
                            course_code_dict[key]['name'] + ';' + course_code_dict[key]['start'] + ';' + course_code_dict[key]['end']
                            for key in list(course_code_dict.keys())
                        ]
                        inlines_keyboard = []
                        for i in evt_name_list:
                            inlines_keyboard.append([InlineKeyboardButton(text=i, callback_data=i)])
                        keyboard = InlineKeyboardMarkup(inline_keyboard=inlines_keyboard)
                        self.bot.sendMessage(chat_id, "Your events are as follows in the format: event_name;start_time;end_time")
                        self.bot.sendMessage(chat_id, "Please click the event that you want to remove!", reply_markup=keyboard)

                elif msg_received == '/getevent':
                    excel = db.DB()
                    course_code_str = excel.table_query(chat_id, other_event_id=True)[4]
                    if not excel.isRecordExist(chat_id, other_event_id=True) or course_code_str is None:
                        self.bot.sendMessage(chat_id, "There is no event recorded in our database!")
                        self.bot.sendMessage(chat_id, self.suggestion)
                        self.bot.sendMessage(chat_id, "Run /addevent to add an event")
                    
                    else:
                        course_code_dict = json.loads(course_code_str)
                        evt_name_list = [
                            course_code_dict[key]['name'] + ';' + course_code_dict[key]['start'] + ';' + course_code_dict[key]['end']
                            for key in list(course_code_dict.keys())
                        ]
                        inlines_keyboard = []
                        for i in evt_name_list:
                            inlines_keyboard.append([InlineKeyboardButton(text=i, callback_data=i)])
                        keyboard = InlineKeyboardMarkup(inline_keyboard=inlines_keyboard)
                        self.bot.sendMessage(chat_id, "Your events are as follows in the format: \n *event_name;start_time;end_time*", parse_mode="Markdown", reply_markup=keyboard)
                        self.bot.sendMessage(chat_id, "What you probably want do next: ")
                        self.bot.sendMessage(chat_id, "Run /removeevent to remove an event")
                        self.bot.sendMessage(chat_id, "Run /addevent to add an event")
                        self.bot.sendMessage(chat_id, "Run /getevent to list all events you have added")
                
                elif msg_received == '/setstudenttype':
                    self.bot.sendMessage(chat_id,'Are you a full time or part time student?',reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Full Time"), KeyboardButton(text="Part Time")]],one_time_keyboard=True))

                elif msg_received == '/addcourse':
                    self.bot.sendMessage(chat_id, 'Sure thing')
                    print(response)
                    check_db = db.DB()
                    first_week_exist = check_db.isRecordExist(chat_id, first_week=True)
                    first_recess_week_exist = check_db.isRecordExist(chat_id, first_recess_week=True)
                    student_type_exist = check_db.isRecordExist(chat_id, student_type=True)
                    is_satisfied = [first_week_exist, first_recess_week_exist, student_type_exist]
                    if not all(is_satisfied):
                        # any of the requirements are not satisfied
                        self.bot.sendMessage(chat_id,'Hmm... Wait a second. You haven\'t told me enough data!')
                        self.bot.sendMessage(chat_id,'Run /setstudenttype to set your student type, i.e. Full Time or Part Time')
                        self.bot.sendMessage(chat_id, 'Run /addfirstweek to set your first_week and first_recess_week')
                        self.error = 1  # explicitly telling that there is an error
                    else:
                        self.bot.sendMessage(chat_id, "Please type your course code below. For example, CZ1003")
                        print(response)
                        self.error = 0  # no error occured
                
                elif msg_received == '/removecourse':
                    excel = db.DB()
                    course_code_str = excel.table_query(chat_id, course_code_event_id=True)[3]
                    if not excel.isRecordExist(chat_id, course_code_event_id=True) or course_code_str is None:
                        self.bot.sendMessage(chat_id,"There is nothing to remove...")
                        self.bot.sendMessage(chat_id, self.suggestion)
                        self.bot.sendMessage(chat_id, "Run /addcourse to add a course")
                    
                    else:
                        course_code_dict = json.loads(course_code_str)
                        course_code_list = [
                            key
                            for key in sorted(list(course_code_dict.keys()))
                        ]
                        inlines_keyboard = []
                        for i in course_code_list:
                            inlines_keyboard.append([InlineKeyboardButton(text=i, callback_data=i)])
                        keyboard = InlineKeyboardMarkup(inline_keyboard=inlines_keyboard)
                        self.bot.sendMessage(chat_id, "Please click the course that you want to remove!",reply_markup=keyboard)
                
                elif msg_received == '/getcourse':
                    excel = db.DB()
                    course_code_str = excel.table_query(chat_id, course_code_event_id=True)[3]
                    if not excel.isRecordExist(chat_id, course_code_event_id=True) or course_code_str is None:
                        self.bot.sendMessage(chat_id, "There are no indexes registered in our database!")
                        self.bot.sendMessage(chat_id, self.suggestion)
                        self.bot.sendMessage(chat_id, "Run /addcourse to add your index")
                    else:
                        course_code_dict = json.loads(course_code_str)
                        course_code_list = [
                            key
                            for key in sorted(list(course_code_dict.keys()))
                        ]
                        inlines_keyboard = []
                        for i in list(course_code_list):
                            inlines_keyboard.append([InlineKeyboardButton(text=i, callback_data=i)])
                        keyboard = InlineKeyboardMarkup(inline_keyboard=inlines_keyboard)
                        self.bot.sendMessage(chat_id, "Your course code are as follows: ", reply_markup=keyboard)
                        self.bot.sendMessage(chat_id, self.suggestion)
                        self.bot.sendMessage(chat_id, "Run /addcourse to add a course")
                        self.bot.sendMessage(chat_id, "Run /removecourse to remove a course (if any)")
                
                elif msg_received == '/quit':
                    self.bot.sendMessage(chat_id, "Bye :(")

                elif msg_received == '/isfree':
                    self.bot.sendMessage(chat_id, "Please enter the date interval using the following format: ")
                    self.bot.sendMessage(chat_id, "YYYY-MM-DD HH:MM;YYYY-MM-DD HH:MM")
                    self.bot.sendMessage(chat_id, '*For example:* ', parse_mode="Markdown")
                    self.bot.sendMessage(chat_id, '2017-10-09 08:00;2017-10-09 16:00', parse_mode="Markdown")
                
                elif msg_received == '/addfirstweek':
                    self.bot.sendMessage(chat_id, "Please enter the Monday dates of your first week and first recess week using the following format: ")
                    self.bot.sendMessage(chat_id, "*FirstWeek;FirstRecessWeek*", parse_mode="Markdown")
                    self.bot.sendMessage(chat_id, '*For example:* ', parse_mode="Markdown")
                    self.bot.sendMessage(chat_id, '_2017-8-14;2017-10-2_', parse_mode="Markdown")
                    self.bot.sendMessage(chat_id, "*Notes*: _These two dates are very important. If you enter the wrong dates and add your course (i.e. by running /addcourse), consequently, your course schedule will be shifted by one or more weeks!_", parse_mode="Markdown")
                
                elif msg_received == '/getupcomingevent':
                    self.bot.sendMessage(chat_id, 'Please enter how many upcoming events are you looking for!')
                    self.bot.sendMessage(chat_id, '*For example:* ', parse_mode="Markdown")
                    self.bot.sendMessage(chat_id, "_10_", parse_mode="Markdown")

                else:
                    self.bot.sendMessage(chat_id, "Command not updated!")

            else:
                
                # Execute the command further
                # Create the Command Object first
                global BotCommandObject
                BotCommandObject = BotCommand(msg['text'])
                # to prevent crashing as it separates the variables so literally it can run parallelly
                # This checks if the last msg['text'] is indeed a command
                if len(self.list_update_message) >= 2 and self.list_update_message[-2] == '/addevent':
                    
                    try:
                        BotCommandObject.AddEventCommand(chat_id)

                    except err.ParseError:
                        self.bot.sendMessage(chat_id, 'Cannot addevent! Make sure to enter the correct format!')
                        self.bot.sendMessage(chat_id, self.suggestion)
                        self.bot.sendMessage(chat_id, "Run /addevent again with the correct time format")
                    
                    except err.IsNotFreeError:
                        self.bot.sendMessage(chat_id, self.suggestion)
                        self.bot.sendMessage(chat_id, "Run /addevent to add another event with different datetime")
                    
                    except err.QueryError:
                        self.bot.sendMessage(chat_id, "Your format is correct, however we cannot perform the query to your Google Account")
                        self.bot.sendMessage(chat_id, "Chances are: ")
                        self.bot.sendMessage(chat_id, '1. You have problems with your API keys')
                        self.bot.sendMessage(chat_id, '2. You entered a bad date, e.g. your end time is smaller than your start time')
                        self.bot.sendMessage(chat_id, self.suggestion)
                        self.bot.sendMessage(chat_id, 'Resolve your API problem')
                        self.bot.sendMessage(chat_id, 'Run /addevent again and give me a reasonable date interval')
                    
                    except:
                        self.bot.sendMessage(chat_id, 'Unknown Error occured')
                    
                    else:
                        self.bot.sendMessage(chat_id, self.successRecordDatabase)
                        self.bot.sendMessage(chat_id, self.suggestion)
                        self.bot.sendMessage(chat_id, "Run /addevent to add another event")
                        self.bot.sendMessage(chat_id, "Run /removeevent to remove an event")
                        self.bot.sendMessage(chat_id, "Run /getevent to list all events you have added")

                elif len(self.list_update_message) >= 2 and (self.list_update_message[-2] == '/setstudenttype' or self.list_update_message[-2] == '/setstudentype' or self.list_update_message[-2] == '/st'):
                    
                    try:
                        BotCommandObject.SetStudentType(chat_id)
                    
                    except:
                        self.bot.sendMessage(chat_id, 'Wrong format!')
                    
                    else:
                        self.bot.sendMessage(chat_id, self.successRecordDatabase,reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                        self.bot.sendMessage(chat_id, "Have you added your first week?")
                        self.bot.sendMessage(chat_id, "If you haven't, run /addfirstweek")
                        self.bot.sendMessage(chat_id, "If you have, then run /addcourse straight away!")

                elif len(self.list_update_message) >= 2 and self.list_update_message[-2] == '/isfree':
                    try:
                        BotCommandObject.IsFreeCommand(chat_id)
                    
                    except err.ParseError:
                        self.bot.sendMessage(chat_id, 'Cannot perform query!')
                        self.bot.sendMessage(chat_id, self.suggestion)
                        self.bot.sendMessage(chat_id, 'Run /isfree again with the correct date format')
                    
                    except err.QueryError:
                        self.bot.sendMessage(chat_id, "Your format is correct, however we cannot perform the query to your Google Account")
                        self.bot.sendMessage(chat_id, "Chances are: ")
                        self.bot.sendMessage(chat_id, '1. You have problems with your API keys')
                        self.bot.sendMessage(chat_id, '2. You entered a bad date, e.g. your end time is smaller than your start time')
                        self.bot.sendMessage(chat_id, self.suggestion)
                        self.bot.sendMessage(chat_id, 'Resolve your API problem')
                        self.bot.sendMessage(chat_id, 'Run /addevent again and give me a reasonable date interval')
                    
                    except err.IsNotFreeError:
                        self.bot.sendMessage(chat_id, self.suggestion)
                        self.bot.sendMessage(chat_id, "Run /isfree again with different datetime")
                    else:
                        self.bot.sendMessage(chat_id, 'You are free on this time interval')
                        self.bot.sendMessage(chat_id, self.suggestion)
                        self.bot.sendMessage(chat_id, 'Run /addevent to add an event for this interval time')
                        self.bot.sendMessage(chat_id, 'Run /getevent to list all events you have added')
                        self.bot.sendMessage(chat_id, 'Run /isfree again to check for another time')
                
                elif len(self.list_update_message) >= 2 and self.list_update_message[-2] == '/addcourse' and not self.error:
                    
                    self.bot.sendMessage(chat_id, 'Please wait while we process your information. This may take around a minute.\n')
                    self.bot.sendMessage(chat_id, 'To prevent crashing, please wait until the Success message has appeared.\n')
                    try:
                        self.indexchosen=''
                        BotCommandObject.AddCourseCommand(chat_id)
                        self.parseddataindex = BotCommandObject.parseddataindex
                    
                    except err.BrowserError:
                        self.bot.sendMessage(chat_id, 'Cannot access the course!')
                        self.bot.sendMessage(chat_id, 'Chances are: ')
                        self.bot.sendMessage(chat_id, '1. You have problems with your browser driver (e.g. chromedriver for Google Chrome)')
                        self.bot.sendMessage(chat_id, '2. You entered a course code that does not exist')
                        self.bot.sendMessage(chat_id, self.suggestion)
                        self.bot.sendMessage(chat_id, 'Resolve your browser problem')
                        self.bot.sendMessage(chat_id, 'Run /addcourse again and enter the correct course code')
                    except:
                        self.bot.sendMessage(chat_id, 'Cannot access the course! Make sure you have entered the correct format!')
                        self.bot.sendMessage(chat_id, self.suggestion)
                        self.bot.sendMessage(chat_id, "Run /addcourse again and enter the correct course code")

                    else:
                        if not self.error:
                            self.bot.sendMessage(chat_id, "The indexes for this course code has been successfully accessed. Please do the instructions above :)")

                elif len(self.list_update_message) >= 2 and self.list_update_message[-2] == '/addfirstweek':
                    try:
                        BotCommandObject.AddFirstWeek(chat_id)
                    except err.IsNotMondayError:
                        self.bot.sendMessage(chat_id, "The input date is not Monday!")
                        self.bot.sendMessage(chat_id, self.failRecordDatabase)
                        self.bot.sendMessage(chat_id, "Please run /addfirstweek again and enter the Monday dates of your first week and first recess week!")
                    except err.ParseError:
                        self.bot.sendMessage(chat_id, 'Unable to parse!')
                        self.bot.sendMessage(chat_id, self.failRecordDatabase)
                        self.bot.sendMessage(chat_id, self.suggestion)
                        self.bot.sendMessage(chat_id, 'Run /addfirstweek again and enter the correct format!')

                    else:
                        self.bot.sendMessage(chat_id, self.successRecordDatabase)
                        self.bot.sendMessage(chat_id, "Have you set your student type?")
                        self.bot.sendMessage(chat_id, "If you haven't, run /setstudenttype")
                        self.bot.sendMessage(chat_id, "If you have, run /addcourse straight away!")
                
                elif len(self.list_update_message) >= 2 and self.list_update_message[-2] == '/getupcomingevent':
                    try:
                        BotCommandObject.getUpcomingEvent(chat_id)
                    except ValueError:
                        self.bot.sendMessage(chat_id, "Wrong format")
                        self.bot.sendMessage(chat_id, self.suggestion)
                        self.bot.sendMessage(chat_id, "Run /getupcomingevent again and enter an integer")
                else:

                    # Below is not a command. It only makes the bot smarter
                    # manual emoticons ONLY :p
                    if msg_received[0] == ':':
                        
                        if len(msg_received) <= 3:
                            self.bot.sendMessage(chat_id, msg['text'])
                        
                        else:
                            self.bot.sendMessage(chat_id, "What is that??? .-.")
                    elif msg_received.find('rude') != -1:
                        self.bot.sendMessage(chat_id, BotReply().reply_dict['rude'])
                    
                    # If the bot knows reply the message
                    elif BotReply().isValidtoReply(msg_received):
                        print(BotReply().reply_dict[msg_received])

                        # With name?
                        if BotReply().isWithName(msg_received):
                            self.bot.sendMessage(chat_id, BotReply().reply_dict[msg_received] +', ' + msg['chat']['first_name'] + ' !')
                                        
                        elif msg_received == 'meetings':
                            self.bot.sendMessage(chat_id, BotReply().reply_dict[msg_received])
                            inlines_keyboard = []
                            
                            for i in range(len(hc.PreformattedBotInlineMarkup().days)):
                                inlines_keyboard.append([InlineKeyboardButton(text=hc.PreformattedBotInlineMarkup().days[i], callback_data=hc.PreformattedBotInlineMarkup().days[i])])
                            keyboard = InlineKeyboardMarkup(inline_keyboard=inlines_keyboard)
                            self.bot.sendMessage(chat_id, 'Choose a day!', reply_markup=keyboard)
                        
                        else:
                            self.bot.sendMessage(chat_id, BotReply().reply_dict[msg_received])
                
                    else:
                        self.bot.sendMessage(chat_id, "Sorry, I don't know what to reply such conversation yet. :'(")

    def on_callback_query(self, msg):
        query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')
        print('Callback Query:', query_id, chat_id, query_data)
        if msg['message']['text'].find('Please choose your index below')!=-1:
            try:
                self.indexchosen = query_data
                BotFindIndexObject = hc.chooseindex()
                BotFindIndexObject.selectindex(self.indexchosen, self.parseddataindex)
            except:
                self.bot.answerCallbackQuery(query_id, text='Error! :(')
                self.bot.sendMessage(chat_id, 'Error occured! Please try again...')
            else:
                self.bot.answerCallbackQuery(query_id, text='Index added! :)')

            BotFindIndexObject = hc.chooseindex()
            complete_data = BotFindIndexObject.selectindex(self.indexchosen, self.parseddataindex)
            course_code_dict = {
                course_code: {
                    'index':self.indexchosen,
                    'event_id': []
                }
            }
            # Check if the dictionary already exists
            db_check = db.DB()
            if db_check.isRecordExist(chat_id, course_code_event_id=True):
                data = db_check.table_query(chat_id, course_code_event_id=True)[3]
                data_dict = json.loads(data)
                if(course_code in list(data_dict.keys())):
                    self.bot.sendMessage(chat_id, 'Our database shows that you have already added the course code %s' %(course_code))
                    self.bot.sendMessage(chat_id, 'You cannot add the same course code twice!')
                    self.bot.sendMessage(chat_id, 'To change index, you must remove current existing course code by running /removecourse!')
                    self.bot.sendMessage(chat_id, "Typo? Just run /addcourse again and type the correct course code")
                    raise err.QueryError
                course_code_dict.update(data_dict)

            if not BotCommandObject.error:
                # If online course is selected
                if complete_data['recurrence'][0].find('Online') != -1:
                    self.bot.answerCallbackQuery(query_id, text='It is an online course!')
                    self.bot.sendMessage(chat_id, "%s is an online course! No need to add it to your Google Calendar!" %(course_code))
                    self.bot.sendMessage(chat_id, self.failRecordDatabaseandCalendar)
                    self.bot.sendMessage(chat_id, self.suggestion)
                    self.bot.sendMessage(chat_id, "Run /addcourse to add another course (no online course, please)")
                    self.bot.sendMessage(chat_id, "Run /removecourse to remove a course")
                    self.bot.sendMessage(chat_id, "Run /getcourse to list all the courses you have added")
                
                else:
                    # Initialize pre requisite before adding to Google Calendar
                    toGoogle = IndexToGoogle(chat_id, complete_data)
                    event_list = toGoogle.get_event()
                    # Loads the dictionary to the database
                    course_code_dict_str = json.dumps(course_code_dict)
                    db.DB().update(chat_id, course_code_event_id=course_code_dict_str)
                    try:
                        toGoogle.PreCreateEventIndex(event_list, self.indexchosen)
                    
                    except:
                        self.bot.sendMessage(chat_id, "You have credential issues")
                        self.bot.sendMessage(chat_id, self.failRecordDatabaseandCalendar)
                        self.bot.sendMessage(chat_id, self.suggestion)
                        self.bot.sendMessage(chat_id, "Fix your API issues and put your credential files in the correct location")
                        self.bot.sendMessage(chat_id, "If necessary, delete your entire API project and create another one by following the instructions in the [Google's official documentation](https://developers.google.com/google-apps/calendar/quickstart/python)", parse_mode="Markdown")
                        # Delete from database
                        del(course_code_dict[course_code])
                        course_code_str = json.dumps(course_code_dict)
                        db.DB().update(chat_id, course_code_event_id=course_code_str)
                        
                    else:
                        self.bot.sendMessage(chat_id, "Nice!")
                        self.bot.sendMessage(chat_id, "%s (index %s) has been added to your Google Calendar and our database" %(course_code, query_data))
                        self.bot.sendMessage(chat_id, self.suggestion)
                        self.bot.sendMessage(chat_id, "Run /addcourse to add another course")
                        self.bot.sendMessage(chat_id, "Run /removecourse to remove a course")
                        self.bot.sendMessage(chat_id, "Run /getcourse to list all the courses you have added")
                    
        elif msg['message']['text'].find('Please click the course that you want to remove!') != -1:
            try:
                BotCommand(query_data).RemoveCourseCommand(chat_id)
            
            except:
                self.bot.sendMessage(chat_id, self.failRemoveDatabaseandCalendar)
                self.bot.answerCallbackQuery(query_id, text='Error! :(')

            else:
                self.bot.answerCallbackQuery(query_id, text='Course removed! :)')
                self.bot.sendMessage(chat_id, self.successRemoveDatabaseandCalendar)
                self.bot.sendMessage(chat_id, self.suggestion)
                self.bot.sendMessage(chat_id, "Run /addcourse to replace your removed course, if you wish")
                self.bot.sendMessage(chat_id, "Run /removecourse to remove another course")
                self.bot.sendMessage(chat_id, "Run /getcourse to list all the courses you have added")

        elif msg['message']['text'].find("Please click the event that you want to remove!") != -1:
            self.bot.answerCallbackQuery(query_id, text='Removing event...')
            try:
                BotCommand(query_data).RemoveEventCommand(chat_id)
            except:
                self.bot.sendMessage(chat_id, "Cannot remove event, unknown error happens!")
                self.bot.sendMessage(chat_id, self.failRecordDatabaseandCalendar)
            else:
                self.bot.sendMessage(chat_id, "The event %s has been removed!" %(query_data))
                self.bot.sendMessage(chat_id, self.successRemoveDatabaseandCalendar)
                self.bot.sendMessage(chat_id, self.suggestion)
                self.bot.sendMessage(chat_id, "Run /removeevent to remove another event")
                self.bot.sendMessage(chat_id, "Run /addevent to add an event")
                self.bot.sendMessage(chat_id, "Run /getevent to list all events you have added")
        elif msg['message']['text'].find("Your course code are as follows") != -1:
            self.bot.answerCallbackQuery(query_id,'')
        else:
            self.bot.answerCallbackQuery(query_id, text='')
            
    def StoreChat(self, update_object):
        update_id = update_object[0]['update_id']
        text = update_object[0]['message']['text']
        
        # A simple dictionary {update_id: 'text'}
        self.db_chat[update_id] = text

        # only the text
        self.list_update_message = list(self.db_chat.values())


class BotReply(API):
    """This is a class for Replies"""
    def __init__(self):
        super().__init__()
        self.reply_dict = {
            'hi': 'Hi',
            'hi bot': 'Hi',
            'hey': 'Hey',
            'hello': 'Hello',
            'good morning': 'Good morning',
            'good afternoon': 'Good afternoon',
            'good evening': 'Good evening',
            'good night': 'Good night',
            'good day': 'Good day',
            'who created you?': 'Awesome people named Jason, Hans, Audrey, Gaby, and Dennis :)',
            'who created you': 'Awesome people named Jason, Hans, Audrey, Gaby, and Dennis :)',
            'where are you from?': 'I was made at NTU Singapore :) Pretty cool isn\'t it?',
            'where are you from': 'I was made at NTU Singapore :) Pretty cool isn\'t it?',
            'how old are you?': 'I was made sometime in early September 2017',
            'how old are you': 'I was made sometime in early September 2017',
            'what are you doing?': 'Replying you. Duh.',
            'what are you doing': 'Replying you. Duh.',
            'what are you?': 'I\'m a bot :))',
            'what are you': "I'm a bot :))",
            'what do you do?': 'type in /start to know :)',
            'what do you do': 'type in /start to know :)',
            'who are you?': "i'm a bot :))",
            'who are you': "i'm a bot :))",
            'thanks': 'no problem!',
            'oh thanks': 'no problem!',
            'ok thanks': 'no problem!',
            'rude': 'sry :(',
            "what's your name": "not sure hahah sry call me bot",
            "what's your name?": "not sure hahah sry call me bot",
            "what is your name?": "not sure hahah sry call me bot",
            "what is your name": "not sure hahah sry call me bot",
            'hey bot': "yep?",
            'im bored': "I'm not sure I can help you with that. Sorry :(",
            "i'm bored": "I'm not sure I can help you with that. Sorry :(",
            'course': "Feeling productive are we? Okay, let's get started",
            'meetings': "Feeling productive are we? Okay, let's get started",
        }
        #  Trivia: dictionary accessing time is close to O(1), while list is O(n), hence better use dictionary when n is big, won't affect if n is small tho
        self.reply_with_name = [
            'hi',
            'hi bot',
            'hey',
            'hello',
            'good morning',
            'good afternoon',
            'good evening',
            'good night',
            'good day',
        ]

    def isValidtoReply(self, msg):
        return msg in self.reply_dict

    def isWithName(self, msg):
        return msg in self.reply_with_name


class BotCommand(API):
    """This is a class for Commands"""
    
    def __init__(self, str_text):
        super().__init__()
        self.command_list = [
            '/start',
            '/help',
            '/quit',
            '/isfree',
            '/getupcomingevent',
            '/addevent',
            '/removeevent',
            '/getevent',
            '/addcourse',
            '/removecourse',
            '/getcourse',
            '/setstudenttype',
            '/addfirstweek',
        ]
        self.str_text = str_text
        
        # Updatable
        self._start_busy = None
        self._end_busy = None
        self.getdata = hc.splintergetdata()  # property not yet added!!!

    @property
    def start_busy(self):
        return self._start_busy

    @property
    def end_busy(self):
        return self._end_busy

    @start_busy.setter
    def start_busy(self, value):
        self._start_busy = value

    @end_busy.setter
    def end_busy(self, value):
        self._end_busy = value

    def isValidCommand(self):
        return self.str_text in self.command_list

    def AddEventCommand(self, chat_id):
        try:
            # Parsing
            str_input = hc.StringParseGoogleAPI(self.str_text)
            str_input.ParseEvent()
            event_name = str_input.event_name
            location = str_input.location
            start_date = str_input.start_date
            start_date_pretty = str_input.start_time_cantik
            end_date_pretty = str_input.end_time_cantik
            end_date = str_input.end_date

        except:
            raise err.ParseError
        
        try:
            # Performing queries
            Google = gc.GoogleAPI()
            query = Google.FreeBusyQuery(start_date_pretty, end_date_pretty)
            isFree = Google.isFree(query)
            info_busy = Google.BusyInfo(query)
        
        except:
            raise err.QueryError('Unable to perform query')
        
        # Get the query's busy info
        if not isFree:
            print("not free!")
            self.bot.sendMessage(chat_id, "Cannot add event!")
            self.bot.sendMessage(chat_id, "You have %d event(s) occuring between %s and %s" %(len(info_busy), start_date_pretty, end_date_pretty))
            
            for i in range(len(info_busy)):
                # Ignoring timezones
                ignored_tz_start_busy = hc.StringParseGoogleAPI(info_busy[i]['start']).IgnoreTimeZone()
                ignored_tz_end_busy = hc.StringParseGoogleAPI(info_busy[i]['end']).IgnoreTimeZone()

                # Make these pretty
                start_busy_pretty = ignored_tz_start_busy.strftime('%Y-%m-%d %H:%M')
                end_busy_pretty = ignored_tz_end_busy.strftime('%Y-%m-%d %H:%M')

                # Send message to user
                self.bot.sendMessage(chat_id, "%d. %s until %s" %(i + 1, start_busy_pretty, end_busy_pretty))
            
            # Raise the error
            raise err.IsNotFreeError
        
        else:
            # Call the GoogleAPI class and create event
            current_event_id = gc.GoogleAPI().createEvent(event_name, location, start_date, end_date)
            # load the event to the database
            other_event_id_dict = {
                current_event_id: {
                    'name': event_name,
                    'location': location,
                    'start': start_date_pretty,
                    'end': end_date_pretty
                }
            }
            excel = db.DB()
            existing_data_str = excel.table_query(chat_id, other_event_id=True)[4]
            if excel.isRecordExist(chat_id, other_event_id=True):
                existing_data_dict = json.loads(existing_data_str)
                other_event_id_dict.update(existing_data_dict)

            other_event_id_str = json.dumps(other_event_id_dict)
            excel.update(chat_id, other_event_id=other_event_id_str)
            
    def RemoveEventCommand(self, chat_id):
        query_data = self.str_text
        evt_name, start, end = query_data.split(';')
        excel = db.DB()
        other_event_id_str = excel.table_query(chat_id, other_event_id=True)[4]
        other_event_id_dict = json.loads(other_event_id_str)
        for key in list(other_event_id_dict.keys()):
            if other_event_id_dict[key]['name'] == evt_name and other_event_id_dict[key]['start'] == start and other_event_id_dict[key]['end'] == end:
                evt_id = key
        
        del(other_event_id_dict[evt_id])
        other_event_id_update_str = json.dumps(other_event_id_dict)
        excel.update(chat_id, other_event_id=other_event_id_update_str)
        gc.GoogleAPI().deleteEvent(evt_id)

    def IsFreeCommand(self, chat_id):
        try:
            start_date_query, end_date_query = self.str_text.split(';')
        except:
            raise err.ParseError

        # Call the GoogleAPI class and check isFree
        try:
            query = gc.GoogleAPI().FreeBusyQuery(start_date_query, end_date_query)
            isFree = gc.GoogleAPI().isFree(query)
        except:
            raise err.QueryError

        self.bot.sendMessage(chat_id, isFree)
        # Get the query's busy info
        if not isFree:
            info_busy = gc.GoogleAPI().BusyInfo(query)
            self.bot.sendMessage(chat_id, 'You are busy on this time interval!')
            self.bot.sendMessage(chat_id, "You have %d event(s) occuring between %s and %s" %(len(info_busy), start_date_query, end_date_query))
            for i in range(len(info_busy)):
                # Ignoring timezones
                ignored_tz_start_busy = hc.StringParseGoogleAPI(info_busy[i]['start']).IgnoreTimeZone()
                ignored_tz_end_busy = hc.StringParseGoogleAPI(info_busy[i]['end']).IgnoreTimeZone()

                # Make these pretty
                start_busy_pretty = ignored_tz_start_busy.strftime('%Y-%m-%d %H:%M')
                end_busy_pretty = ignored_tz_end_busy.strftime('%Y-%m-%d %H:%M')

                # Send message to user
                self.bot.sendMessage(chat_id, "%d. %s until %s" %(i + 1, start_busy_pretty, end_busy_pretty))
            raise err.IsNotFreeError
        return isFree

    def AddCourseCommand(self,chat_id):
        global course_code  # set course_code to global!
        course_code = self.str_text.replace(' ', '').upper()
        if len(course_code) < 3:
            raise err.ParseError
        excel = db.DB()
        student_type = excel.table_query(chat_id, student_type=True)[2]
        is_course_code_exist = excel.isRecordExist(chat_id, course_code_event_id=True)
        course_code_str = excel.table_query(chat_id, course_code_event_id=True)[3]
        
        if course_code_str is None:
            excel.update(chat_id, course_code_event_id='{}')
        course_code_str_update = excel.table_query(chat_id, course_code_event_id=True)[3]
        course_code_dict = json.loads(course_code_str_update)
        
        if not is_course_code_exist or course_code not in list(course_code_dict.keys()):
            # Splinter in action
            try:
                self.getdata.start(course_code, student_type)
                self.parseddataindex = self.getdata.parsedatahml()
            except:
                raise err.BrowserError

            inlines_keyboard = []
            for i in range(len(self.getdata.indexlist)):
                inlines_keyboard.append([InlineKeyboardButton(text=self.getdata.indexlist[i], callback_data=self.getdata.indexlist[i])])

            keyboard = InlineKeyboardMarkup(inline_keyboard=inlines_keyboard)
            self.bot.sendMessage(chat_id, 'Please choose your index below.\n Click only one of them once!', reply_markup=keyboard)
        else:
            API.error = 1
            self.bot.sendMessage(chat_id, 'Our database shows that you have already added the course code %s' %(course_code))
            self.bot.sendMessage(chat_id, 'You cannot add the same course code twice!')
            self.bot.sendMessage(chat_id, 'To change index, you must remove current existing course code by running /removecourse!')
            self.bot.sendMessage(chat_id, "Typo? Just run /addcourse again and enter the correct course code")

    def RemoveCourseCommand(self, chat_id):
        course_code = self.str_text
        print(course_code)
        
        check_db = db.DB()
        course_code_db_str = check_db.table_query(chat_id, course_code_event_id=course_code)[3]
        course_code_db_obj = json.loads(course_code_db_str)

        # Remove it from Google Calendar
        Google = gc.GoogleAPI()
        try:
            for evt_id in course_code_db_obj[course_code]['event_id']:
                Google.deleteEvent(evt_id)
        except:
            self.error = 1
            raise ValueError
        
        # Remove it from the database
        if not self.error:
            del(course_code_db_obj[course_code])
            updated_course_code_str = json.dumps(course_code_db_obj)
            check_db.update(chat_id, course_code_event_id=updated_course_code_str)

    def SetStudentType(self, chat_id):
        str_input = hc.StringParseStudentType(self.str_text)
        str_input.ParseInput()
        # print(self.str_text)
        course_type = str_input.course_type
        print(course_type)
        excel = db.DB()
        excel.update(chat_id, student_type=course_type)

    def AddFirstWeek(self, chat_id):
        try:
            first_week, first_recess_week = self.str_text.split(';')
        except:
            raise err.ParseError
        first_week_obj = datetime.datetime.strptime(first_week, '%Y-%m-%d')
        first_recess_week_obj = datetime.datetime.strptime(first_recess_week, '%Y-%m-%d')
        # If it is Monday, then proceed
        if first_week_obj.weekday() == 0 and first_recess_week_obj.weekday() == 0:
            # Initialize db
            excel = db.DB()
            # Update the exel file
            excel.update(chat_id, first_week=first_week, first_recess_week=first_recess_week)
        else:
            raise err.IsNotMondayError('Date is not monday!')
    
    def getUpcomingEvent(self, chat_id):
        num_event = int(self.str_text)
        self.bot.sendMessage(chat_id, 'Getting %s upcoming event(s) for you' %(num_event))
        events = gc.GoogleAPI().getUpcomingEventList(num_event)
        event_detail = ''
        if not events:
            self.bot.sendMessage(chat_id, 'No upcoming events found!')
            self.bot.sendMessage(chat_id, self.suggestion)
            self.bot.sendMessage(chat_id, 'Run /addevent to add an event')
        else:
            if num_event > len(events):
                self.bot.sendMessage(chat_id, 'There are only %d event(s) ahead!' %(len(events)))
            self.bot.sendMessage(chat_id, "Here they are!")
            for event in events:
                # Getting the start, end, and summary
                start = event['start']['dateTime']
                end = event['end']['dateTime']
                summary = event['summary']

                # Ignoring their timezones
                ignore_tz_start = hc.StringParseGoogleAPI(start).IgnoreTimeZone()
                ignore_tz_end = hc.StringParseGoogleAPI(end).IgnoreTimeZone()

                # Making these pretty
                ignore_tz_start_pretty = ignore_tz_start.strftime('%Y-%m-%d %H:%M')
                ignore_tz_end_pretty = ignore_tz_end.strftime('%Y-%m-%d %H:%M')

                # Combining all
                complete_event = "*" + summary + "*" + ' (' + ignore_tz_start_pretty + ' until ' + ignore_tz_end_pretty + ') \n'
                event_detail += complete_event
            
            try:
                self.bot.sendMessage(chat_id, event_detail, parse_mode="Markdown")
            except:
                self.bot.sendMessage(chat_id, 'Too many events! Enter a smaller integer please!')
                self.bot.sendMessage(chat_id, self.suggestion)
                self.bot.sendMessage(chat_id, "Run /getupcomingevent again and enter a smaller integer, typically less than 70!")
        

class IndexToGoogle(API):
    """Description: the main class to integrate indexes with Google Calendar"""
    def __init__(self, chat_id, index_dictionary):
        super().__init__()
        self.index_dictionary = index_dictionary
        self.chat_id = chat_id
    
    def get_event(self):
        """Description: Get each a list event data from the parsed HTML
        Return: list
        """
        value_list = list(self.index_dictionary.values())
        key_list = list(self.index_dictionary.keys())
        event_list = [[] for event in range(len(value_list[0]))]  # initialize list of lists
        ParseObject = hc.StringParseGoogleAPI(self.index_dictionary)
        for i in range(len(value_list[0])):
            # Change the time format
            time = self.index_dictionary['time'][i]
            formated_time = ParseObject.ParseDateIndex(time)
            self.index_dictionary['time'][i] = formated_time

            # Change the day format
            day = self.index_dictionary['day'][i]
            # Setting the value
            ParseObject.day = day
            # Assign it to the list
            self.index_dictionary['day'][i] = ParseObject.day
            for key in key_list:
                event_list[i].append(self.index_dictionary[key][i])
        return event_list

    def PreCreateEventIndex(self, evt_list, fixed_index):
        """Description: preparation to add the event from evt_list to Google Calendar"""
        course_index = fixed_index  # This is a fixed index
        for i in range(len(evt_list)):
            event1 = evt_list[i]
            course_type = event1[1]
            course_group = event1[2]
            day = event1[3]
            start_time = event1[4][0]
            end_time = event1[4][1]
            location = event1[5]
            recurrence = event1[6]
            first_week = db.DB().table_query(self.chat_id, first_week=True)[0]
            first_recess_week = db.DB().table_query(self.chat_id, first_recess_week=True)[1]

            # Concatenate together
            event_summary = " ".join([course_code, course_type])
            event_desc = " ".join([course_index, course_group])

            ignore_first_event = False
            if day != 'MO':
                if recurrence.count('1') != 0 or recurrence != '' or recurrence.count('1') == 0:
                    ignore_first_event = True
            
            # Recurrence Parsing
            recurrenceObject = hc.StringParseGoogleAPI(recurrence)
            recurrence_string = recurrenceObject.ParseOccurIgnoreWeek(first_week, start_time)
            
            # CreateEventIndex
            gc.GoogleAPI().CreateEventIndex(self.chat_id, event_summary, location, event_desc, start_time, end_time, first_week, first_recess_week, recurrence_string, day, ignore_first_event)
