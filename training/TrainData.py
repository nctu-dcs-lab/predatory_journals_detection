import csv
import os
import numpy as np
import sys
import numba
import random


wordvector = []
trainX = []
trainY = []
testX = []
testY = []
TrainData = []
TestData = []
with open('C:/Users/DCS-LAB/Desktop/thesis/dataset/preprocess/JournalVector.csv', newline='', encoding='utf8') as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        wordvector.append(row)
with open('C:/Users/DCS-LAB/Desktop/thesis/dataset/preprocess/journal_dataset/trainx.csv', newline='', encoding='utf8') as csvfile2:
    rows = csv.reader(csvfile2)
    for row in rows:
        trainX.append(row)
with open('C:/Users/DCS-LAB/Desktop/thesis/dataset/preprocess/journal_dataset/testx.csv', newline='', encoding='utf8') as csvfile3:
    rows = csv.reader(csvfile3)
    for row in rows:
        testX.append(row)

random.shuffle(trainX[0])
random.shuffle(testX[0])
for k in range(1636):  # 掠奪性期刊LABEL設:0 好期刊LABEL設:1
    tr_x = int(trainX[0][k])
    array = wordvector[tr_x]
    TrainData.append(array)
    if tr_x < 833:
        trainY.append(0)
    else:
        trainY.append(1)
for j in range(410):
    te_x = int(testX[0][j])
    array = wordvector[te_x]
    TestData.append(array)
    if te_x < 833:
        testY.append(0)
    else:
        testY.append(1)


with open('Train_X.csv', 'w', newline='') as csvFile:  # 寫入CSV檔
    writer = csv.writer(csvFile)
    writer.writerows(TrainData)

with open('Train_Y.csv', 'w', newline='') as csvFile2:  # 寫入CSV檔
    writer = csv.writer(csvFile2)
    writer.writerow(trainY)

with open('Test_X.csv', 'w', newline='') as csvFile3:  # 寫入CSV檔
    writer = csv.writer(csvFile3)
    writer.writerows(TestData)

with open('Test_Y.csv', 'w', newline='') as csvFile4:  # 寫入CSV檔
    writer = csv.writer(csvFile4)
    writer.writerow(testY)
