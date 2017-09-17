import splinter
import selenium
import sys
import time
import telepot

from pyvirtualdisplay import Display
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver

#display = Display(visible=0, size=(800, 600))
#display.start()


binary = FirefoxBinary('C:\\Program Files\\Nightly\\firefox.exe', log_file=sys.stdout)
driver = webdriver.Firefox(firefox_binary=binary)
driver.get("https://intoli.com/blog/email-spy/")
heading_element = driver.find_element_by_xpath('//*[@id="heading-breadcrumbs"]')
if heading_element:
    print(heading_element.get_property('textContent').strip())
else:
    print("Heading element not found!")
driver.close()