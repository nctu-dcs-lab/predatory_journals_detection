import numpy as np
import csv
import matplotlib.pyplot as plt
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.metrics import recall_score, precision_score
from sklearn.neighbors import KNeighborsClassifier


def precision(predict, TestY):
    pj = 0
    correct = 0
    for i in range(410):
        if predict[i] == '0':
            pj += 1
        if predict[i] == '0' and TestY[i] == '0':
            correct += 1
    return correct / pj


def recall(predict, TestY):
    pj = 0
    correct = 0
    for i in range(410):
        if TestY[i] == '0':
            pj += 1
        if predict[i] == '0' and TestY[i] == '0':
            correct += 1
    return correct / pj


def f1score(P, R):
    F1 = 2*P*R/(P+R)
    return F1

keyword = np.load('850_keyword.npy')
TrainX = []
TrainY = []
TestX = []
TestY = []
with open('Train_X.csv', newline='') as trx:
    rows = csv.reader(trx)
    for row in rows:
        TrainX.append(row)
with open('Train_Y.csv', newline='') as tr_y:
    rows = csv.reader(tr_y)
    for row in rows:
        TrainY.append(row)
with open('Test_X.csv', newline='') as tx:
    rows = csv.reader(tx)
    for row in rows:
        TestX.append(row)
with open('Test_Y.csv', newline='') as ty:
    rows = csv.reader(ty)
    for row in rows:
        TestY.append(row)

TrainX = np.array(TrainX).astype(np.float)
TrainY = np.array(TrainY)
TestX = np.array(TestX).astype(np.float)
TestY = np.array(TestY)
TrainY = TrainY.ravel()
TestY = TestY.ravel()
while True:
    mode = input('1: Naive_Bayes, 2: Multinomial Naive Bayes, 3: SVM, 4: Stochastic Gradient Descent, '
                 '5: Logistic Regression, 6: RandomForestClassifier, 7: VotingClassifier, 8: KNN\n')
    if mode == '0':
        break
    elif mode == '1':
        gnb = GaussianNB()
        gnb.fit(TrainX, TrainY)
        predict = gnb.predict(TestX)
        print('預測:', predict)
        print('-' * 60)
        print('正確率:', gnb.score(TestX, TestY))
        p = precision(predict, TestY)
        r = recall(predict, TestY)
        f1 = f1score(p, r)
        print('Precision:', p)
        print('Recall:', r)
        print('F-Measure:', f1)
        print('-' * 60)
    elif mode == '2':
        MNB = MultinomialNB()
        MNB.fit(TrainX, TrainY)
        predict = MNB.predict(TestX)
        print('預測:', predict)
        print('-' * 60)
        print('正確率:', MNB.score(TestX, TestY))
        p = precision(predict, TestY)
        r = recall(predict, TestY)
        f1 = f1score(p, r)
        print('Precision:', p)
        print('Recall:', r)
        print('F-Measure:', f1)
        print('-' * 60)
    elif mode == '3':
        svm = SVC(kernel='linear', probability=True)
        svm.fit(TrainX, TrainY)
        predict = svm.predict(TestX)
        print('預測:', predict)
        print('-' * 60)
        print('正確率:', svm.score(TestX, TestY))
        p = precision(predict, TestY)
        r = recall(predict, TestY)
        f1 = f1score(p, r)
        print('Precision:', p)
        print('Recall:', r)
        print('F-Measure:', f1)
        print('-' * 60)
    elif mode == '4':
        sgd = SGDClassifier()
        sgd.fit(TrainX, TrainY)
        predict = sgd.predict(TestX)
        print('預測:', predict)
        print('-' * 60)
        print('正確率:', sgd.score(TestX, TestY))
        p = precision(predict, TestY)
        r = recall(predict, TestY)
        f1 = f1score(p, r)
        print('Precision:', p)
        print('Recall:', r)
        print('F-Measure:', f1)
        print('-' * 60)
    elif mode == '5':
        LR = LogisticRegression(solver='liblinear')
        LR.fit(TrainX, TrainY)
        predict = LR.predict(TestX)
        print('預測:', predict)
        print('-' * 60)
        print('正確率:', LR.score(TestX, TestY))
        p = precision(predict, TestY)
        r = recall(predict, TestY)
        f1 = f1score(p, r)
        print('Precision:', p)
        print('Recall:', r)
        print('F-Measure:', f1)
        print('-' * 60)
    elif mode == '6':
        RFC = RandomForestClassifier(n_estimators=50, random_state=1)
        RFC.fit(TrainX, TrainY)
        predict = RFC.predict(TestX)
        print('預測:', predict)
        print('-' * 60)
        print('正確率:', RFC.score(TestX, TestY))
        p = precision(predict, TestY)
        r = recall(predict, TestY)
        f1 = f1score(p, r)
        print('Precision:', p)
        print('Recall:', r)
        print('F-Measure:', f1)
        print('-' * 60)
        from sklearn import tree
        from sklearn.tree import export_graphviz
        estimator = RFC.estimators_[25]
        export_graphviz(estimator,out_file = 'tree2.dot',feature_names = keyword,class_names = TrainY,rounded = True, proportion = False,precision = 2, filled = True)
    elif mode == '7':
        clf1 = GaussianNB()
        clf2 = MultinomialNB()
        clf3 = SVC(kernel='linear', probability=True)
        clf4 = SGDClassifier()
        clf5 = LogisticRegression(solver='liblinear')
        clf6 = RandomForestClassifier(n_estimators=50, random_state=1)
        hardvote = VotingClassifier(
            estimators=[('gnb', clf1), ('mnb', clf2), ('svm', clf3), ('sgd', clf4), ('lr', clf5), ('rf', clf6)],
            voting='hard')
        hardvote = hardvote.fit(TrainX, TrainY)
        predict = hardvote.predict(TestX)
        print('預測:', predict)
        print('-' * 60)
        print('正確率:', hardvote.score(TestX, TestY))
        p = precision(predict, TestY)
        r = recall(predict, TestY)
        f1 = f1score(p, r)
        print('Precision:', p)
        print('Recall:', r)
        print('F-Measure:', f1)
        print('-' * 60)
    elif mode == '8':
        error_rate = []
        min_error = 1
        min_knn = 1
        for i in range(1, 60):
            knn = KNeighborsClassifier(n_neighbors=i)
            knn.fit(TrainX, TrainY)
            pred_i = knn.predict(TestX)
            error_rate.append(np.mean(pred_i != TestY))
            print(np.mean(pred_i != TestY))
            if min_error > np.mean(pred_i != TestY):
                min_error = np.mean(pred_i != TestY)
                min_knn = i
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, 60), error_rate, color='blue', linestyle='dashed', marker='o', markerfacecolor='red',
                 markersize=10)
        plt.title('Error Rate vs. K Value')
        plt.xlabel('K')
        plt.ylabel('Error Rate')
        plt.savefig('knn_error_rate.png')  # save picture
        plt.show()  # 4最小
        print(min_error)
        knn = KNeighborsClassifier(n_neighbors=min_knn)
        knn.fit(TrainX, TrainY)
        predict = knn.predict(TestX)
        print('預測:', predict)
        print('-' * 60)
        print('正確率:', knn.score(TestX, TestY))
        p = precision(predict, TestY)
        r = recall(predict, TestY)
        f1 = f1score(p, r)
        print('Precision:', p)
        print('Recall:', r)
        print('F-Measure:', f1)
        print('-' * 60)