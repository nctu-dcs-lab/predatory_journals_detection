import csv
import os
import numpy as np
import sys
import numba


@numba.jit
def get_tfidf(BOW, key_tf, key_tf_idf, bad_text_num, good_text_num, alltext_num):  # 算SPAM跟GENUINE的TF-IDF
    for i in range(len(BOW[0])):
        if key_tf[i][0] != 0:
            key_tf_idf[i][0] = (key_tf[i][0] / bad_text_num) * np.log10(alltext_num / key_tf[i][0])
        else:
            key_tf_idf[i][0] = (key_tf[i][0] / bad_text_num) * 0
        if key_tf[i][1] != 0:
            key_tf_idf[i][1] = (key_tf[i][1] / good_text_num) * np.log10(alltext_num / key_tf[i][1])
        else:
            key_tf_idf[i][1] = 0
    return key_tf_idf

maxInt = sys.maxsize
while True:
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

BOW = []
with open('C:/Users/DCS-LAB/Desktop/thesis/dataset/preprocess/journal_dataset/BOW.csv', newline='', encoding = 'utf8') as bag_of_word:  # 讀取BOW字典
    rows = csv.reader(bag_of_word)
    for row in rows:
        BOW.append(row)
key_tf = np.zeros((len(BOW[0]), 2))
key_tf_idf = np.zeros((len(BOW[0]), 2))
bad_text_num = 0  # 掠奪性期刊總共有幾個字詞
good_text_num = 0  # 好期刊總共有幾個字詞
filepath = 'C:/Users/DCS-LAB/Desktop/thesis/dataset/preprocess/keyword/SpamGenuine_tf_idf.npy'
if os.path.isfile(filepath):
    key_tf_idf = np.load('keyword/SpamGenuine_tf_idf.npy')
    diff = np.load('keyword/keyword_tfidf.npy')
else:
    alltext_num = 0
    journal_text = []
    with open('C:/Users/DCS-LAB/Desktop/thesis/dataset/preprocess/journal_dataset/traindata.csv', newline='', encoding='utf8') as csvfile4:  # 算全部有幾個字詞
        rows = csv.reader(csvfile4)
        for row in rows:
            num = len(row)
            alltext_num += num
            journal_text.append(row)
    for i in range(len(journal_text)):  # 算此單字出現幾次
        if i < 666:
            num = len(journal_text[i])
            bad_text_num += num
            tmp = 0
            for Bow_word in BOW[0]:
                for content_word in journal_text[i]:  # 期刊裡的內容(字詞)
                    if content_word == Bow_word:
                        key_tf[tmp][0] += 1
                tmp += 1
        else:
            num = len(journal_text[i])
            good_text_num += num
            tmp = 0
            for Bow_word in BOW[0]:
                for content_word in journal_text[i]:
                    if content_word == Bow_word:
                        key_tf[tmp][1] += 1
                tmp += 1

    key_tf_idf = get_tfidf(BOW, key_tf, key_tf_idf, bad_text_num, good_text_num, alltext_num)
    np.save('keyword/SpamGenuine_tf_idf', key_tf_idf)

    diff = np.zeros(len(BOW[0]))
    for k in range(len(BOW[0])):  # 計算SPAM-GENUINE的分數
        diff[k] = key_tf_idf[k][0] - key_tf_idf[k][1]
    np.save('keyword/keyword_tfidf', diff)

wordnum = int(input('BOW_num:'))
tmp = 0
getword = np.argsort(-diff)
important_word = []
for i in getword:
    if tmp < wordnum and len(BOW[0][i]) > 1:  # 取前50-9000名的字詞當作重要字詞
        print(BOW[0][i], diff[i])
        important_word.append(BOW[0][i])
        tmp += 1
np.save('keyword/' + str(wordnum) + '_keyword', important_word)
print(tmp)