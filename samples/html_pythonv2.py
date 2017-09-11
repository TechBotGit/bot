import splinter
import selenium
from bs4 import BeautifulSoup
from splinter import Browser
#geckodriver must be installed!!!
#browser = Browser('firefox')
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
    html_page=browser.html # no need anymore, can be deleted
    #print(html_page) #debug catch html
    #print(browser.url)#debug url
    #print(html)
    alls=browser.find_by_id("ui_body_container")
    #bb= driver.find_elements_by_id("ui_body_container")
    print(alls)
    print(alls.value)
    alls=alls.find_by_value("")
    print(alls)
    print(alls.value)
    #print(alls.name)
    z=0
    for i in alls:
        z+=1
        print(z)
        cur=alls.find_by_value("")
        print(type(cur))
        print(cur)
        print(cur.value)
        #print(cur.name)
        #print(cur.value)
        #print(cur.value)
    #print(all)
    while 1:
        a=input()
        break
    if browser.is_element_present_by_value('2017-2018 Semester 1',5) :
        browser.find_by_value('2017-2018 Semester 1').first.click()
    html_page=browser.html
    print(browser.html)
    print(browser.url)
    #element = browser.find_by_css('value').first
    #print(element.value)
    #with open(html_page) as fp:
     #   print("test")
    soup = BeautifulSoup(html_page)
    print(soup)
    while 1:
        a=input()
        break
    
