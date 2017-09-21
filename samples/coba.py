
from bs4 import BeautifulSoup
import urllib.request

schedule = urllib.request.urlopen('file:///C:/Users/Dennis%20Stevanus/Desktop/Class%20Schedule.html').read()

soup = BeautifulSoup(schedule,'lxml')

tables = soup.find('table',border=True)

rows = tables.find_all('tr')

first_columns = []
second_columns = []
third_columns = []
fourth_columns = []
fifth_columns = []
sixth_columns = []

index_num="10104"
finish=False

for iterator in range(1,len(rows)):
    first_columns.append(rows[iterator].find_all('td')[0])
    second_columns.append(rows[iterator].find_all('td')[1])
    third_columns.append(rows[iterator].find_all('td')[2])
    fourth_columns.append(rows[iterator].find_all('td')[3])
    fifth_columns.append(rows[iterator].find_all('td')[4])
    sixth_columns.append(rows[iterator].find_all('td')[5])


for iterator in range(len(first_columns)):
    if first_columns[iterator].text==index_num:
        # print(first_columns[iterator].text)
        for iterator2 in range(iterator,len(first_columns)):
            if first_columns[iterator2].text!='' and first_columns[iterator2].text!=index_num:
                finish=True
                break
            print(second_columns[iterator2].text,third_columns[iterator2].text,fourth_columns[iterator2].text,fifth_columns[iterator2].text,sixth_columns[iterator2].text)
            
    if finish:
        break
