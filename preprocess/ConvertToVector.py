import csv
import os
import numpy as np
import sys
import numba


wordnum = int(input('BOW_num:'))
keyword = np.load('keyword/' + str(wordnum) + '_keyword.npy')
print(keyword)
journal_vector = []
with open('allj_content.csv', newline='', encoding='utf8') as csvfile:  # 把每個期刊轉換成前word_num名字詞的VECTOR
    rows = csv.reader(csvfile)
    for row in rows:
        wordvector = np.zeros(len(keyword))
        for text in row:
            for i in range(len(keyword)):
                if keyword[i] == text:
                    wordvector[i] = 1
        journal_vector.append(wordvector)

with open('JournalVector.csv', 'w', newline='', encoding = 'utf8') as csvFile2:
    writer = csv.writer(csvFile2)
    writer.writerows(journal_vector)

print(journal_vector)
