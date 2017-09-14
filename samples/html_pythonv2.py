import os
import sys
import time
import telepot
import splinter
import selenium
import time #for checking runtime
from bs4 import BeautifulSoup
from splinter import Browser
#geckodriver must be installed!!!
#browser = Browser('firefox')
start_time = time.time()
with Browser() as browser:
    url = "https://wish.wis.ntu.edu.sg/webexe/owa/aus_schedule.main"
    browser.visit(url)
    html_page=browser.html
    list_of_course=BeautifulSoup(html_page,'html.parser')
    #print(list_of_course)
    #list2_of_course=list_of_course.find_all('select')
    #print(list2_of_course)
    #print(type(list2_of_course))
    listofcourse=list()
    list_of_course=list_of_course.find_all("option")
    #convert beautifulsoup results to readable list
    while len(list_of_course)>0 :
        #if list_of_course[0].value=="":
        #print(list_of_course[0].string)
        stringtemp=list_of_course[0].string
        if stringtemp.find("20")==-1 and stringtemp.find("---")==-1:
            stringtemp=stringtemp.replace("\n","")
            if stringtemp!="" and len(stringtemp)>1:
                listofcourse.append(stringtemp)
        #else:
            #print(stringtemp)
        list_of_course.pop(0)
    print(listofcourse)
    print(len(listofcourse))
    a=0
    for i in range(len(listofcourse)):
        print(i)
        #if browser.is_element_present_by_text(listofcourse[i]) :
        print(listofcourse[i])
        browser.find_option_by_text(listofcourse[i]).first.click()
        browser.find_by_value('Load Class Schedule').first.click()
        #browser.windows.current=browser.windows[1]
        while len(browser.windows)>1:
            for ii in browser.windows :
                if ii.url=="https://wish.wis.ntu.edu.sg/webexe/owa/AUS_SCHEDULE.main_display1":
                    browser.windows.current=ii
                    html_page=browser.html
                    #print(html_page)
                    print(a,listofcourse[i])
                    a+=1
                    soup = BeautifulSoup(html_page,'html.parser')
                    ii.close()
        #browser.windows.current.close()
        #browser.windows.current = browser.windows[0]
        browser.back()
    print("a=",a)
print("--- %s seconds ---" % (time.time() - start_time))