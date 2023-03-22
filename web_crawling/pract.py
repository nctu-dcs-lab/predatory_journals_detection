from selenium import webdriver
from bs4 import BeautifulSoup
import string
import numpy as np
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import nltk
import re
from nltk.stem import WordNetLemmatizer
from nltk.stem import SnowballStemmer
import numpy as np
import random


'''driver = webdriver.PhantomJS(executable_path=r'C:/Users/DCS-LAB/phantomjs-2.1.1-windows/bin/phantomjs')  # PhantomJs
driver.get('https://zygoscient.org/') # 輸入範例網址，交給瀏覽器
pageSource = driver.page_source  # 取得網頁原始碼
soup = BeautifulSoup(pageSource, 'lxml')
pretty = soup.prettify() # 把網頁內碼編排整齊
print(pretty)'''
punc = string.punctuation
print(punc)
list = ['asd.', '123.5', 'b', 'c', '你', 'ph.d']
tmp = 0
aa = 0
strh = "fsadfds                    rwerewqr          hgjghfjgf"
qq = strh.split()
print(qq)
tmp = 0
for i in list:
    tmp += 1
print(tmp)
ar = [[2,2,2],[5,5,5]]
fg = np.array([3,3,3])
ar = np.array(ar)
ar = ar * fg
print(ar)
p = re.compile('[^a-z^A-Z^0-9^.]')
stry = 'My name is 你好. asss ddw zz? 你好嗎? 我很好123.444 Vol.4'
print(p.split(stry))
ttt = 'abcdef'
print(ttt[3:])
'''while True:
    if list[tmp] == 'b':
        del list[tmp]
        print(list[tmp])
    else:
        tmp += 1
    strh += list[aa]
    length = len(list[aa])
    if list[aa].isalnum() == True:
        print(list[aa].upper())
    if list[aa][length - 1] == '.':
        list[aa] = list[aa][:length - 1]
    if list[aa].isalnum() == True:
        print(list[aa].upper())
    aa += 1
    if aa == 6:
        break
print(list[:3])'''
'''st = strh.split(' ')
for i in st:
    if i != '':
        print(i.upper())
tmp = 5
count = 0'''
'''while count != tmp:
    print('a')
    count += 1'''
