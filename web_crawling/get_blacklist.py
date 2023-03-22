from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import numpy as np
driver = webdriver.PhantomJS(executable_path=r'C:/Users/DCS-LAB/phantomjs-2.1.1-windows/bin/phantomjs')  # PhantomJs
driver.get('https://beallslist.net/standalone-journals/') # 輸入範例網址，交給瀏覽器 https://beallslist.net/standalone-journals/  https://predatoryjournals.com/journals/
pageSource = driver.page_source  # 取得網頁原始碼
soup = BeautifulSoup(pageSource, 'lxml')
beall_blacklist = []
for link in soup.find_all('a'):
    beall_blacklist.append(link.get('href'))
    #print(link.get('href'))
print(beall_blacklist)
with open('beall_blacklist.csv', 'w', newline='', encoding = 'utf8') as csvFile:  # 寫入CSV檔
    writer = csv.writer(csvFile)
    writer.writerow(beall_blacklist)
driver.close()