import matplotlib.pyplot as plt
import numpy as np
import csv
from matplotlib.ticker import MultipleLocator

while True:
    mode = input('which mode(GNB, MNB, LR, RF, SGD, SVM, Voting, KNN, 3Voting, no1Voting): ')
    accuracy = []
    pricision = []
    recall = []
    overall = []
    f1score = []
    FN = []
    X = []
    great_a = 0
    great_p = 0
    great_r = 0
    great_s = 0
    great_f = 0
    great_acc = 0
    great_pre = 0
    great_rec = 0
    great_f1 = 0
    great_fn = 100
    for i in range(50, 9001, 50):
        X.append(i)
    with open(mode + '.csv', newline='', encoding='utf8') as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            overall.append(row)
    for k in range(len(overall)):
        for i in range(len(overall[k])):
            if i == 0:
                accuracy.append(float(overall[k][i]))
                if great_acc < accuracy[k]:
                    great_acc = accuracy[k]
                    great_a = (k+1)*50
            elif i == 1:
                pricision.append(float(overall[k][i]))
                if great_pre < pricision[k]:
                    great_pre = pricision[k]
                    great_p = (k+1)*50
            elif i == 2:
                recall.append(float(overall[k][i]))
                if great_rec < recall[k]:
                    great_rec = recall[k]
                    great_r = (k+1)*50
                f1score.append(2*float(pricision[k])*float(recall[k])/(float(pricision[k])+float(recall[k])))
                if great_f1 < f1score[k]:
                    great_f1 = f1score[k]
                    great_s = (k+1)*50
            else:
                FN.append(float(overall[k][i]))
                if great_fn > FN[k]:
                    great_fn = FN[k]
                    great_f = (k+1)*50
    print(great_a)
    print(great_acc)
    print(great_p)
    print(great_pre)
    print(great_r)
    print(great_rec)
    print(great_s)
    print(great_f1)
    print(great_f)
    print(great_fn)
    for j in range(4):
        chance = ''
        plt.xlabel('Num of BOW')
        plt.ylabel('Probability')
        if j == 0:
            plt.title('Accuracy')
            plt.plot(X, accuracy)
            chance = 'accuracy'
        elif j == 1:
            plt.title('Precision')
            plt.plot(X, pricision)
            chance = 'precision'
        elif j == 2:
            plt.title('Recall')
            plt.plot(X, recall)
            chance = 'recall'
        elif j == 3:
            plt.title('F1_Score')
            plt.plot(X, f1score)
            chance = 'f1score'
        plt.savefig('C:/Users/DCS-LAB/Desktop/thesis/dataset/training/picture/' + mode + '_' + chance + '.png')
        plt.show()
    plt.xlabel('Num of BOW')
    plt.ylabel('Num of FN')
    plt.title('FN')
    plt.plot(X, FN)
    plt.savefig('C:/Users/DCS-LAB/Desktop/thesis/dataset/training/picture/' + mode + '_' + 'FN' + '.png')
    plt.show()