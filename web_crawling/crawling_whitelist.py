from selenium import webdriver
from bs4 import BeautifulSoup
import csv


def del_tag(all_text): # 把網頁去標籤化,只留文字部分(script & css都不要)
    content = []
    css_or_script = 0 # 判斷是否為script or css
    for j in range(len(all_text)):
        if css_or_script == 0:  # 之前沒遇到script or css
            if all_text[j] != '':
                if all_text[j][0] == '<':
                    if len(all_text[j]) > 5:
                        if all_text[j][1] == 's' and all_text[j][2] == 't' and all_text[j][3] == 'y' and all_text[j][4] == 'l' and all_text[j][5] == 'e':
                            css_or_script = 1  # 如果是css  css_or_script = 1
                    if len(all_text[j]) > 6:
                        if all_text[j][1] == 's' and all_text[j][2] == 'c' and all_text[j][3] == 'r' and all_text[j][4] == 'i' and all_text[j][5] == 'p' and all_text[j][6] == 't':
                            css_or_script = 1  # 如果是script  css_or_script = 1
                    if len(all_text[j]) > 8:
                        if all_text[j][1] == 'n' and all_text[j][2] == 'o' and all_text[j][3] == 's' and all_text[j][4] == 'c' and all_text[j][5] == 'r' and all_text[j][6] == 'i' and all_text[j][7] == 'p' and all_text[j][8] == 't':
                            css_or_script = 1  # 如果是noscript  css_or_script = 1

                    if len(all_text[j]) > 9:
                        if all_text[j][1] == '!' and all_text[j][2] == '-' and all_text[j][3] == '-' and all_text[j][4] == '<':
                            if all_text[j][5] == 's' and all_text[j][6] == 't' and all_text[j][7] == 'y' and all_text[j][8] == 'l' and all_text[j][9] == 'e':
                                css_or_script = 1  # 如果是css  css_or_script = 1
                            if len(all_text[j]) > 10:
                                if all_text[j][5] == 's' and all_text[j][6] == 'c' and all_text[j][7] == 'r' and all_text[j][8] == 'i' and all_text[j][9] == 'p' and all_text[j][10] == 't':
                                    css_or_script = 1  # 如果是script  css_or_script = 1
                            if len(all_text[j]) > 12:
                                if all_text[j][5] == 'n' and all_text[j][6] == 'o' and all_text[j][7] == 's' and all_text[j][8] == 'c' and all_text[j][9] == 'r' and all_text[j][10] == 'i' and all_text[j][11] == 'p' and all_text[j][12] == 't':
                                    css_or_script = 1  # 如果是noscript  css_or_script = 1
                else:  # 如果為內容時 把他加入到content
                    last = len(all_text[j])
                    if all_text[j][0] != '&' and all_text[j][last-1] != '>':
                        content.append(all_text[j])
        elif css_or_script == 1:  # 他是script or css裡的內容物，因此全部都不需要
            if all_text[j] != '':
                if len(all_text[j]) > 6:
                    if all_text[j][0] == '<' and all_text[j][1] == '/':  # 判斷是否為結尾 是的話就把 css_or_script = 0
                        if all_text[j][2] == 's' and all_text[j][3] == 't' and all_text[j][4] == 'y' and all_text[j][5] == 'l' and all_text[j][6] == 'e':
                            css_or_script = 0
                        if len(all_text[j]) > 7:
                            if all_text[j][2] == 's' and all_text[j][3] == 'c' and all_text[j][4] == 'r' and all_text[j][5] == 'i' and all_text[j][6] == 'p' and all_text[j][7] == 't':
                                css_or_script = 0
                        if len(all_text[j]) > 9:
                            if all_text[j][2] == 'n' and all_text[j][3] == 'o' and all_text[j][4] == 's' and all_text[j][5] == 'c' and all_text[j][6] == 'r' and all_text[j][7] == 'i' and all_text[j][8] == 'p' and all_text[j][9] == 't':
                                css_or_script = 0
    return content


driver = webdriver.PhantomJS(executable_path=r'C:/Users/DCS-LAB/phantomjs-2.1.1-windows/bin/phantomjs')  # PhantomJs

journal_url = []  # 好期刊網站
all_ju_content = []
with open('whitelist.csv', newline='') as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        journal_url.append(row[8])
for ju in journal_url:
    driver.get(ju) # 輸入範例網址，交給瀏覽器
    pageSource = driver.page_source  # 取得網頁原始碼
    soup = BeautifulSoup(pageSource, 'lxml')
    pretty = soup.prettify() # 把網頁內碼編排整齊
    all_text = pretty.split('\n')
    for i in range(len(all_text)):  # 去掉空格
        all_text[i] = all_text[i].strip()
    content = del_tag(all_text)  # 去標籤化
    all_ju_content.append(content)

with open('whitelist_dataset.csv', 'w', newline='', encoding = 'utf8') as csvFile:  # 寫入CSV檔
    writer = csv.writer(csvFile)
    writer.writerows(all_ju_content)
driver.close()  # 關閉瀏覽器
