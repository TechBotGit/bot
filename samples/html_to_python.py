import splinter
import selenium
import sys
import time
import telepot
from bs4 import BeautifulSoup
from splinter import Browser
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
#geckodriver must be installed!!!
#browser = Browser('firefox')
listofsem=list()
def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    tuples=tuple(listofsem)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Press me', callback_data='press')],[InlineKeyboardButton(text='Press me too', callback_data='press 2')]])
    bot.sendMessage(chat_id, 'Use inline keyboard', reply_markup=keyboard)

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)
    bot.answerCallbackQuery(query_id, text='Got it')

f=open("a.txt","r")
TOKEN= (f.read())
f.close()
bot = telepot.Bot(TOKEN)
    
f=open("personal.txt","r")
user=f.readline()
password=f.readline()
f.close()
with Browser() as browser:
    # Visit URL
    url = "https://www.ntu.edu.sg/Students/Undergraduate/AcademicServices/CourseRegistration/Pages/default.aspx"
    browser.visit(url)
    browser.click_link_by_partial_text('Print/Check Courses Registered')
    browser.fill('UserName', user)
    domain=browser.select('Domain', 'STUDENT')
    if domain!='STUDENT':
        browser.select('Domain', 'STUDENT')
    browser.find_by_name('bOption').first.click()
    browser.fill('PIN',password)
    browser.find_by_name('bOption').first.click()
    html_page=browser.html
    listsem = BeautifulSoup(html_page,'html.parser')
    #print(listsem)
    getsem = listsem.find_all('input',value=True,type="button")
    #print(type(getsem))
    #print(getsem)
    while len(getsem)>0 :
        print(getsem[0]['value'])
        listofsem.append(getsem[0]['value'])
        #print(type(getsem[0]['value']))
        getsem.pop(0)
    #print(type(listofsem))
    print(listofsem)
    MessageLoop(bot, {'chat': on_chat_message,'callback_query': on_callback_query}).run_as_thread()
    print('Listening ...')
    while 1:
        time.sleep(10)
    if browser.is_element_present_by_value('2017-2018 Semester 1',5) :
        browser.find_by_value('2017-2018 Semester 1').first.click()
    html_page=browser.html
    soup = BeautifulSoup(html_page,'html.parser')
    #print(soup)
    while 1:
        a=input()
        break
    
