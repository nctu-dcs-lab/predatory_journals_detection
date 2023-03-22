import csv
import numpy as np
import sys
import random
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.neighbors import KNeighborsClassifier


def precision(predict, TestY):
    pj = 0
    correct = 0
    for i in range(410):
        if predict[i] == 0:
            pj += 1
        if predict[i] == 0 and TestY[i] == 0:
            correct += 1
    if pj == 0:
        pj = 1
    return correct / pj


def recall(predict, TestY):
    pj = 0
    correct = 0
    for i in range(410):
        if TestY[i] == 0:
            pj += 1
        if predict[i] == 0 and TestY[i] == 0:
            correct += 1
    if pj == 0:
        pj = 1
    return correct / pj


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

all_journal = []
with open('allj_content.csv', newline='', encoding='utf8') as csvfile:  # 把每個期刊轉換成前word_num名字詞的VECTOR
    rows = csv.reader(csvfile)
    for row in rows:
        all_journal.append(row)
trainX = []
testX = []
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

key_tf = np.zeros((len(BOW[0]), 2))
key_tf_idf = np.zeros((len(BOW[0]), 2))
bad_text_num = 0
good_text_num = 0
diff = np.load('keyword/keyword_tfidf.npy')
wordnum = 50
gnball = []
mnball =[]
svmall = []
sgdall = []
lrall =[]
rfall = []
vall = []
knnall = []
vno1all = []
v3all = []
while True:
    tmp = 0
    getword = np.argsort(-diff)
    important_word = []
    for i in getword:
        if tmp < wordnum and len(BOW[0][i]) > 1:  # 取前50-9000名的字詞當作重要字詞(+50)
            important_word.append(BOW[0][i])
            tmp += 1
    journal_vector = []
    for k in range(len(all_journal)):
        wordvector = np.zeros(len(important_word))
        for text in all_journal[k]:
            for i in range(len(important_word)):
                if important_word[i] == text:
                    wordvector[i] = 1
        journal_vector.append(wordvector)
    TrainData = []
    TestData = []
    trainY = []
    testY = []
    for k in range(1636):  # 掠奪性期刊LABEL設:0 好期刊LABEL設:1
        tr_x = int(trainX[0][k])
        array = journal_vector[tr_x]
        TrainData.append(array)
        if tr_x < 833:
            trainY.append(0)
        else:
            trainY.append(1)
    for j in range(410):
        te_x = int(testX[0][j])
        array = journal_vector[te_x]
        TestData.append(array)
        if te_x < 833:
            testY.append(0)
        else:
            testY.append(1)

    TrainX = np.array(TrainData).astype(np.float)
    TrainY = np.array(trainY)
    TestX = np.array(TestData).astype(np.float)
    TestY = np.array(testY)
    TrainY = TrainY.ravel()
    TestY = TestY.ravel()
    print(wordnum)
    print('-'*60)
    for i in range(10):
        tmparray = []
        if i == 0:
            gnb = GaussianNB()
            gnb.fit(TrainX, TrainY)
            predict = gnb.predict(TestX)
            count = 0
            for fn in range(len(predict)):
                if predict[fn] == 1 and TestY[fn] == 0:
                    count += 1
            accuracy = gnb.score(TestX, TestY)
            print('正確率:', accuracy)
            tmparray.append(accuracy)
            p = precision(predict, TestY)
            r = recall(predict, TestY)
            tmparray.append(p)
            tmparray.append(r)
            tmparray.append(count)
            print('Precision:', p)
            print('Recall:', r)
            print('-' * 60)
            gnball.append(tmparray)
        elif i == 1:
            MNB = MultinomialNB()
            MNB.fit(TrainX, TrainY)
            predict = MNB.predict(TestX)
            count = 0
            for fn in range(len(predict)):
                if predict[fn] == 1 and TestY[fn] == 0:
                    count += 1
            accuracy = MNB.score(TestX, TestY)
            print('正確率:', accuracy)
            tmparray.append(accuracy)
            p = precision(predict, TestY)
            r = recall(predict, TestY)
            tmparray.append(p)
            tmparray.append(r)
            tmparray.append(count)
            print('Precision:', p)
            print('Recall:', r)
            print('-' * 60)
            mnball.append(tmparray)
        elif i == 2:
            svm = SVC(kernel='linear', probability=True)
            svm.fit(TrainX, TrainY)
            predict = svm.predict(TestX)
            count = 0
            for fn in range(len(predict)):
                if predict[fn] == 1 and TestY[fn] == 0:
                    count += 1
            accuracy = svm.score(TestX, TestY)
            print('正確率:', accuracy)
            tmparray.append(accuracy)
            p = precision(predict, TestY)
            r = recall(predict, TestY)
            tmparray.append(p)
            tmparray.append(r)
            tmparray.append(count)
            print('Precision:', p)
            print('Recall:', r)
            print('-' * 60)
            svmall.append(tmparray)
        elif i == 3:
            sgd = SGDClassifier()
            sgd.fit(TrainX, TrainY)
            predict = sgd.predict(TestX)
            count = 0
            for fn in range(len(predict)):
                if predict[fn] == 1 and TestY[fn] == 0:
                    count += 1
            accuracy = sgd.score(TestX, TestY)
            print('正確率:', accuracy)
            tmparray.append(accuracy)
            p = precision(predict, TestY)
            r = recall(predict, TestY)
            tmparray.append(p)
            tmparray.append(r)
            tmparray.append(count)
            print('Precision:', p)
            print('Recall:', r)
            print('-' * 60)
            sgdall.append(tmparray)
        elif i == 4:
            LR = LogisticRegression(solver='liblinear')
            LR.fit(TrainX, TrainY)
            predict = LR.predict(TestX)
            count = 0
            for fn in range(len(predict)):
                if predict[fn] == 1 and TestY[fn] == 0:
                    count += 1
            accuracy = LR.score(TestX, TestY)
            print('正確率:', accuracy)
            tmparray.append(accuracy)
            p = precision(predict, TestY)
            r = recall(predict, TestY)
            tmparray.append(p)
            tmparray.append(r)
            tmparray.append(count)
            print('Precision:', p)
            print('Recall:', r)
            print('-' * 60)
            lrall.append(tmparray)
        elif i == 5:
            RFC = RandomForestClassifier(n_estimators=50, random_state=1)
            RFC.fit(TrainX, TrainY)
            predict = RFC.predict(TestX)
            count = 0
            for fn in range(len(predict)):
                if predict[fn] == 1 and TestY[fn] == 0:
                    count += 1
            accuracy = RFC.score(TestX, TestY)
            print('正確率:', accuracy)
            tmparray.append(accuracy)
            p = precision(predict, TestY)
            r = recall(predict, TestY)
            tmparray.append(p)
            tmparray.append(r)
            tmparray.append(count)
            print('Precision:', p)
            print('Recall:', r)
            print('-' * 60)
            rfall.append(tmparray)
        elif i == 6:
            knn = KNeighborsClassifier(n_neighbors=4)
            knn.fit(TrainX, TrainY)
            predict = knn.predict(TestX)
            count = 0
            for fn in range(len(predict)):
                if predict[fn] == 1 and TestY[fn] == 0:
                    count += 1
            accuracy = knn.score(TestX, TestY)
            print('正確率:', accuracy)
            p = precision(predict, TestY)
            r = recall(predict, TestY)
            tmparray.append(accuracy)
            tmparray.append(p)
            tmparray.append(r)
            tmparray.append(count)
            print('Precision:', p)
            print('Recall:', r)
            print('-' * 60)
            knnall.append(tmparray)
        elif i == 7:
            clf1 = GaussianNB()
            clf2 = MultinomialNB()
            clf3 = SVC(kernel='linear', probability=True)
            clf4 = SGDClassifier()
            clf5 = LogisticRegression(solver='liblinear')
            clf6 = RandomForestClassifier(n_estimators=50, random_state=1)
            clf7 = KNeighborsClassifier(n_neighbors=4)
            hardvote = VotingClassifier(
                estimators=[('gnb', clf1), ('mnb', clf2), ('svm', clf3), ('sgd', clf4), ('lr', clf5), ('rf', clf6), ('knn', clf7)],
                voting='hard')
            hardvote = hardvote.fit(TrainX, TrainY)
            predict = hardvote.predict(TestX)
            count = 0
            for fn in range(len(predict)):
                if predict[fn] == 1 and TestY[fn] == 0:
                    count += 1
            accuracy = hardvote.score(TestX, TestY)
            print('正確率:', accuracy)
            tmparray.append(accuracy)
            p = precision(predict, TestY)
            r = recall(predict, TestY)
            tmparray.append(p)
            tmparray.append(r)
            tmparray.append(count)
            print('Precision:', p)
            print('Recall:', r)
            print('-' * 60)
            vall.append(tmparray)
        elif i == 8:
            clf2 = MultinomialNB()
            clf3 = SVC(kernel='linear', probability=True)
            clf4 = SGDClassifier()
            clf5 = LogisticRegression(solver='liblinear')
            clf6 = RandomForestClassifier(n_estimators=50, random_state=1)
            clf7 = KNeighborsClassifier(n_neighbors=4)
            hardvote = VotingClassifier(
                estimators=[('mnb', clf2), ('svm', clf3), ('sgd', clf4), ('lr', clf5), ('rf', clf6),('knn', clf7)],
                voting='hard')
            hardvote = hardvote.fit(TrainX, TrainY)
            predict = hardvote.predict(TestX)
            count = 0
            for fn in range(len(predict)):
                if predict[fn] == 1 and TestY[fn] == 0:
                    count += 1
            accuracy = hardvote.score(TestX, TestY)
            print('正確率:', accuracy)
            tmparray.append(accuracy)
            p = precision(predict, TestY)
            r = recall(predict, TestY)
            tmparray.append(p)
            tmparray.append(r)
            tmparray.append(count)
            print('Precision:', p)
            print('Recall:', r)
            print('-' * 60)
            vno1all.append(tmparray)
        elif i == 9:
            clf4 = SGDClassifier()
            clf5 = LogisticRegression(solver='liblinear')
            clf6 = RandomForestClassifier(n_estimators=50, random_state=1)
            hardvote = VotingClassifier(
                estimators=[('sgd', clf4), ('lr', clf5), ('rf', clf6)],voting='hard')
            hardvote = hardvote.fit(TrainX, TrainY)
            predict = hardvote.predict(TestX)
            count = 0
            for fn in range(len(predict)):
                if predict[fn] == 1 and TestY[fn] == 0:
                    count += 1
            accuracy = hardvote.score(TestX, TestY)
            print('正確率:', accuracy)
            tmparray.append(accuracy)
            p = precision(predict, TestY)
            r = recall(predict, TestY)
            tmparray.append(p)
            tmparray.append(r)
            tmparray.append(count)
            print('Precision:', p)
            print('Recall:', r)
            print('-' * 60)
            v3all.append(tmparray)
    wordnum += 50
    if wordnum > 9000:
        break

with open('GNB.csv', 'w', newline='') as csvFile:  # 寫入CSV檔
    writer = csv.writer(csvFile)
    writer.writerows(gnball)

with open('MNB.csv', 'w', newline='') as csvFile2:  # 寫入CSV檔
    writer = csv.writer(csvFile2)
    writer.writerows(mnball)

with open('SVM.csv', 'w', newline='') as csvFile3:  # 寫入CSV檔
    writer = csv.writer(csvFile3)
    writer.writerows(svmall)

with open('SGD.csv', 'w', newline='') as csvFile4:  # 寫入CSV檔
    writer = csv.writer(csvFile4)
    writer.writerows(sgdall)

with open('LR.csv', 'w', newline='') as csvFile5:  # 寫入CSV檔
    writer = csv.writer(csvFile5)
    writer.writerows(lrall)

with open('RF.csv', 'w', newline='') as csvFile6:  # 寫入CSV檔
    writer = csv.writer(csvFile6)
    writer.writerows(rfall)

with open('Voting.csv', 'w', newline='') as csvFile7:  # 寫入CSV檔
    writer = csv.writer(csvFile7)
    writer.writerows(vall)

with open('KNN.csv', 'w', newline='') as csvFile8:  # 寫入CSV檔
    writer = csv.writer(csvFile8)
    writer.writerows(knnall)

with open('no1Voting.csv', 'w', newline='') as csvFile9:  # 寫入CSV檔
    writer = csv.writer(csvFile9)
    writer.writerows(vno1all)

with open('3Voting.csv', 'w', newline='') as csvFile10:  # 寫入CSV檔
    writer = csv.writer(csvFile10)
    writer.writerows(v3all)

