import csv
import os
import numpy as np
import sys
import nltk
from nltk.probability import FreqDist


maxInt = sys.maxsize
while True:
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

BOW = []
journals = []
with open('BOW.csv', newline='', encoding = 'utf8') as bag_of_word:  # 讀取BOW字典
    rows = csv.reader(bag_of_word)
    for row in rows:
        BOW.append(row)

with open('pj_content.csv', newline='', encoding = 'utf8') as csvFile2:  # 寫入CSV檔
    rows = csv.reader(csvFile2)
    for row in rows:
        for text in row:
            journals.append(text)

with open('goodj_content.csv', newline='', encoding = 'utf8') as csvFile3:  # 寫入CSV檔
    rows = csv.reader(csvFile3)
    for row in rows:
        for text in row:
            journals.append(text)

fdist = FreqDist(journals)
common = fdist.most_common(1000)
print(common)