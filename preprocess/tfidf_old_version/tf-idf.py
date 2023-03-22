import csv
import os
import numpy as np
import sys


maxInt = sys.maxsize
while True:
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

BOW = []
journals = []
all_journal = []
with open('BOW.csv', newline='', encoding = 'utf8') as bag_of_word:  # 讀取BOW字典
    rows = csv.reader(bag_of_word)
    for row in rows:
        BOW.append(row)

with open('allj_content.csv', newline='', encoding = 'utf8') as journ:  # 讀取BOW字典
    rows = csv.reader(journ)
    for row in rows:
        all_journal.append(row)

print(len(all_journal))
tf = []
idf = np.zeros(len(BOW[0]))
filepath = 'C:/Users/DCS-LAB/Desktop/thesis/dataset/preprocess/journal_wordvector.csv'
if os.path.isfile(filepath):
    print('find')
    with open('journal_wordvector.csv', newline='', encoding='utf8') as csvFile:  # 讀取CSV檔
        rows = csv.reader(csvFile)
        for row in rows:
            journals.append(row)
    with open('tf.csv', newline='', encoding='utf8') as csvFile2:  # 讀取CSV檔
        rows2 = csv.reader(csvFile2)
        for row in rows2:
            tf.append(row)
    idf = np.load('idf.npy')
    tf_idf = np.load('tf_idf.npy')
else:
    print('not find')
    with open('pj_content.csv', newline='', encoding = 'utf8') as pjfile:  # 讀取每個掠奪性網站裡的內容文字
        rows = csv.reader(pjfile)
        for row in rows:
            num = len(row)
            if num == 0:
                num = 1
            word_array = []  # 每個掠奪性網站的word vector
            tf_array = []
            tmp = 0
            for BOW_word in BOW[0]:  # 計算BOW裡的單詞 出現在此掠奪性網站幾次
                count = 0
                for content_word in row:  # 此掠奪性網站的內容文字
                    if content_word == BOW_word:  # 如果此內容文字有對應到BOW裡的單詞 則此BOW的單詞出現數量+1
                        count += 1
                word_array.append(count)  # 記錄此BOW單詞的數量
                tf_array.append(count / num)
                if BOW_word in row:
                    idf[tmp] = idf[tmp] + 1
                tmp += 1
            tf.append(tf_array)
            journals.append(word_array)  # 紀錄此掠奪性網站文字內容對應到BOW的數量
    with open('goodj_content.csv', newline='', encoding = 'utf8') as gjfile:  # 讀取每個掠奪性網站裡的內容文字
        rows = csv.reader(gjfile)
        for row in rows:
            num = len(row)
            if num == 0:
                num = 1
            word_array = []  # 每個掠奪性網站的word vector
            tf_array = []
            tmp = 0
            for BOW_word in BOW[0]:  # 計算BOW裡的單詞 出現在此掠奪性網站幾次
                count = 0
                for content_word in row:  # 此掠奪性網站的內容文字
                    if content_word == BOW_word:  # 如果此內容文字有對應到BOW裡的單詞 則此BOW的單詞出現數量+1
                        count += 1
                word_array.append(count)  # 記錄此BOW單詞的數量
                tf_array.append(count / num)
                if BOW_word in row:
                    idf[tmp] = idf[tmp] + 1
                tmp += 1
            tf.append(tf_array)
            journals.append(word_array)  # 紀錄此掠奪性網站文字內容對應到BOW的數量
    with open('journal_wordvector.csv', 'w', newline='', encoding = 'utf8') as csvFile:  # 寫入CSV檔
        writer = csv.writer(csvFile)
        writer.writerows(journals)

    with open('tf.csv', 'w', newline='', encoding = 'utf8') as csvFile2:  # 寫入CSV檔
        writer = csv.writer(csvFile2)
        writer.writerows(tf)
    np.save('idf', idf)

    tf = np.array(tf, dtype='float64')
    for i in range(len(BOW[0])):
        idf[i] = np.log(len(all_journal) / idf[i])
    tf_idf = np.multiply(tf, idf)
    np.save('tf_idf', tf_idf)
    print(tf_idf)

print(tf_idf)


