import splinter
import selenium
import os
import sys
import time
import telepot
from bs4 import BeautifulSoup
from splinter import Browser
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
#geckodriver must be installed!!!


cek=0
listofsem=list()
returnsem=''


def printtobotlistssem(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    #tuples=tuple(listofsem)
    inlines_keyboard=[[]]
    for i in range(0,len(listofsem)) :
        print(listofsem[i])
        inlines_keyboard.append([InlineKeyboardButton(text=listofsem[i], callback_data=listofsem[i])])
    keyboard = InlineKeyboardMarkup(inline_keyboard=inlines_keyboard)
    bot.sendMessage(chat_id, 's', reply_markup=keyboard)
    print(type(keyboard))
def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)
    returnsem=query_data
    cek=1
    bot.answerCallbackQuery(query_id, text='Got it')


cwd = os.path.dirname(sys.argv[0])
path_file = cwd + '/a.txt'
f = open(path_file, "r")
TOKEN= (f.read())
f.close()
bot = telepot.Bot(TOKEN)
f=open("personal.txt","r")
user=f.readline()
password=f.readline()
f=open("a.txt","r")
TOKEN= (f.read())
f.close()
bot = telepot.Bot(TOKEN)
f=open("personal.txt","r")
user=f.readline()
password=f.readline()
f.close()
with Browser(driver_name='firefox') as browser:
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
    time.sleep(5)
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
    if listofsem[len(listofsem)-1]=='Exit':
        listofsem.pop(len(listofsem)-1)
    print(listofsem)
    MessageLoop(bot, {'chat': printtobotlistssem,'callback_query': on_callback_query}).run_as_thread()
    print('Listening ...')
    while 1:
        if cek==1:
            break
    print("test")
    if browser.is_element_present_by_value(returnsem,5) :
        browser.find_by_value(returnsem).first.click()
    html_page=browser.html
    soup = BeautifulSoup(html_page,'html.parser')
    #print(soup)
    while 1:
        a=input()
        break
    
