import csv
import os
import numpy as np
import sys
import numba
import random


tmp = 0
trainX = []
trainY = []
testX = []
testY = []
while True:  # 隨機取掠奪性期刊的80%當作TRAINING DATA
    number = random.randint(0,832)
    if number not in trainX:
        #print(number)
        trainX.append(number)
        #print(trainX)
        tmp += 1
    if tmp == 666:
        break
tmp = 0
while True:  # 隨機取好期刊的80%當作TRAINING DATA
    number = random.randint(833, 2045)
    if number not in trainX:
        trainX.append(number)
        tmp += 1
    if tmp == 970:
        break
for i in range(2046):
    if i not in trainX:
        testX.append(i)

all_journal = []
with open('C:/Users/DCS-LAB/Desktop/thesis/dataset/preprocess/allj_content.csv', newline='', encoding='utf8') as csvfile:  # 讀取全部期刊
    rows = csv.reader(csvfile)
    for row in rows:
        all_journal.append(row)

Traindata = []
Testdata = []
BOW = []
for i in range(len(trainX)):
    trx = trainX[i]
    array = all_journal[trx]
    Traindata.append(array)
for k in range(len(testX)):
    tx = testX[k]
    array = all_journal[tx]
    Testdata.append(array)

for i in range(len(trainX)):  # 找TRAIN-DATA裡的BOW
    for text in Traindata[i]:
        if text not in BOW:
            BOW.append(text)

with open('trainx.csv', 'w', newline='', encoding = 'utf8') as csvFile2:
    writer = csv.writer(csvFile2)
    writer.writerow(trainX)
with open('testx.csv', 'w', newline='', encoding = 'utf8') as csvFile3:
    writer = csv.writer(csvFile3)
    writer.writerow(testX)
with open('traindata.csv', 'w', newline='', encoding = 'utf8') as csvFile4:
    writer = csv.writer(csvFile4)
    writer.writerows(Traindata)
with open('testdata.csv', 'w', newline='', encoding = 'utf8') as csvFile5:
    writer = csv.writer(csvFile5)
    writer.writerows(Traindata)
with open('BOW.csv', 'w', newline='', encoding = 'utf8') as csvFile6:
    writer = csv.writer(csvFile6)
    writer.writerow(BOW)