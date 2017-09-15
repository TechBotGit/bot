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
browser = Browser('firefox')
#start_time = time.time()
with Browser() as browser:
    url = "https://wish.wis.ntu.edu.sg/webexe/owa/aus_schedule.main"
    browser.visit(url)
    browser.fill("r_subj_code","CZ1005")
    browser.choose("r_search_type","F")
    browser.find_by_value("Search").first.click()
    while len(browser.windows)>0:
        for ii in browser.windows :
            if ii.url=="https://wish.wis.ntu.edu.sg/webexe/owa/AUS_SCHEDULE.main_display1":
                browser.windows.current=ii
                html_page=browser.html
                #print(html_page)
                soup = BeautifulSoup(html_page,'html.parser')
                print(soup)
            ii.close()
