from flask import Flask, render_template, request
import csv
import numpy as np
import random
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from selenium import webdriver
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
from nltk.stem import WordNetLemmatizer
import sys


def del_tag(all_text):  # 把網頁去標籤化,只留文字部分(script & css都不要)
    content = []
    css_or_script = 0  # 判斷是否為script or css
    for j in range(len(all_text)):
        if css_or_script == 0:  # 之前沒遇到script or css
            if all_text[j] != '':
                if all_text[j][0] == '<':
                    if len(all_text[j]) > 5:
                        if all_text[j][1] == 's' and all_text[j][2] == 't' and all_text[j][3] == 'y' and all_text[j][
                            4] == 'l' and all_text[j][5] == 'e':
                            css_or_script = 1  # 如果是css  css_or_script = 1
                    if len(all_text[j]) > 6:
                        if all_text[j][1] == 's' and all_text[j][2] == 'c' and all_text[j][3] == 'r' and all_text[j][
                            4] == 'i' and all_text[j][5] == 'p' and all_text[j][6] == 't':
                            css_or_script = 1  # 如果是script  css_or_script = 1
                    if len(all_text[j]) > 8:
                        if all_text[j][1] == 'n' and all_text[j][2] == 'o' and all_text[j][3] == 's' and all_text[j][
                            4] == 'c' and all_text[j][5] == 'r' and all_text[j][6] == 'i' and all_text[j][7] == 'p' and \
                                all_text[j][8] == 't':
                            css_or_script = 1  # 如果是noscript  css_or_script = 1

                    if len(all_text[j]) > 9:
                        if all_text[j][1] == '!' and all_text[j][2] == '-' and all_text[j][3] == '-' and all_text[j][
                            4] == '<':
                            if all_text[j][5] == 's' and all_text[j][6] == 't' and all_text[j][7] == 'y' and \
                                    all_text[j][8] == 'l' and all_text[j][9] == 'e':
                                css_or_script = 1  # 如果是css  css_or_script = 1
                            if len(all_text[j]) > 10:
                                if all_text[j][5] == 's' and all_text[j][6] == 'c' and all_text[j][7] == 'r' and \
                                        all_text[j][8] == 'i' and all_text[j][9] == 'p' and all_text[j][10] == 't':
                                    css_or_script = 1  # 如果是script  css_or_script = 1
                            if len(all_text[j]) > 12:
                                if all_text[j][5] == 'n' and all_text[j][6] == 'o' and all_text[j][7] == 's' and \
                                        all_text[j][8] == 'c' and all_text[j][9] == 'r' and all_text[j][10] == 'i' and \
                                        all_text[j][11] == 'p' and all_text[j][12] == 't':
                                    css_or_script = 1  # 如果是noscript  css_or_script = 1
                else:  # 如果為內容時 把他加入到content
                    last = len(all_text[j])
                    if all_text[j][0] != '&' and all_text[j][last - 1] != '>':
                        content.append(all_text[j])
        elif css_or_script == 1:  # 他是script or css裡的內容物，因此全部都不需要
            if all_text[j] != '':
                if len(all_text[j]) > 6:
                    if all_text[j][0] == '<' and all_text[j][1] == '/':  # 判斷是否為結尾 是的話就把 css_or_script = 0
                        if all_text[j][2] == 's' and all_text[j][3] == 't' and all_text[j][4] == 'y' and all_text[j][
                            5] == 'l' and all_text[j][6] == 'e':
                            css_or_script = 0
                        if len(all_text[j]) > 7:
                            if all_text[j][2] == 's' and all_text[j][3] == 'c' and all_text[j][4] == 'r' and \
                                    all_text[j][5] == 'i' and all_text[j][6] == 'p' and all_text[j][7] == 't':
                                css_or_script = 0
                        if len(all_text[j]) > 9:
                            if all_text[j][2] == 'n' and all_text[j][3] == 'o' and all_text[j][4] == 's' and \
                                    all_text[j][5] == 'c' and all_text[j][6] == 'r' and all_text[j][7] == 'i' and \
                                    all_text[j][8] == 'p' and all_text[j][9] == 't':
                                css_or_script = 0
    return content


def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return 'a'
    elif tag.startswith('V'):
        return 'v'
    elif tag.startswith('N'):
        return 'n'
    elif tag.startswith('R'):
        return 'r'
    else:
        return 'n'


def preprocess(content):
    content_text = []  # 內容每一行裡的單字
    for text in content:  # 內容裡每行的句子
        after_text = word_tokenize(text)  # 分開英文單字
        for inside_word in after_text:  # 判斷單字是否有停用詞或特殊符號
            if inside_word not in stopword:
                after_split = p.split(inside_word)
                for wo in after_split:
                    if wo != '':
                        if wo != '...':
                            length = len(wo)
                            while True:  # 把最後結尾的.給去掉
                                if length == 0:
                                    break
                                elif wo[0] == '.':
                                    wo = wo[1:length]
                                    length = len(wo)
                                elif wo[length - 1] == '.':
                                    wo = wo[:length - 1]
                                    length = len(wo)
                                else:
                                    break
                            if wo != '':
                                wo = wo.lower()
                                tokens = word_tokenize(wo)
                                pt = nltk.pos_tag(tokens)
                                tag = get_wordnet_pos(pt[0][1])
                                wo = lemmatizer.lemmatize(wo, pos=tag)
                                # print(wo)
                                content_text.append(wo)
    return content_text


def convertword(content_txt):
    global keyword
    wordvector = np.zeros(len(keyword))
    for text in content_txt:
        for i in range(len(keyword)):
            if keyword[i] == text:
                wordvector[i] = 1
    return wordvector


lemmatizer = WordNetLemmatizer()
punc = ['!', '?', ',', ':', '"', '(', ')', '<', '>', '{', '}', '=', '@', '#', '$', '%', '/', '[', ']', '^', '_', '|',
        '+', '-', '*', ';', '~', '&', '©', '–', '”', '“', '…', '—', '→', '.', '’']  # 特殊
stopword = stopwords.words('english')  # 停用詞
p = re.compile('[^a-z^A-Z^0-9^.]')  # 英文跟數字的正規化
for w in punc:
    stopword.append(w)  # 把標點符號加入停用詞

keyword = np.load('C:/Users/DCS-LAB/Desktop/thesis/dataset/preprocess/keyword/850_keyword.npy')
driver = webdriver.PhantomJS(executable_path=r'C:/Users/DCS-LAB/phantomjs-2.1.1-windows/bin/phantomjs')  # PhantomJs
TrainX = []
TrainY = []
spj = []
beall = []
bih = []
history = []
with open('Train_X.csv', newline='') as trx:
    rows = csv.reader(trx)
    for row in rows:
        TrainX.append(row)
with open('Train_Y.csv', newline='') as tr_y:
    rows = csv.reader(tr_y)
    for row in rows:
        TrainY.append(row)
with open('spj_blacklist.csv', newline='', encoding='utf8') as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        spj.append(row)
with open('beall_blacklist.csv', newline='', encoding='utf8') as csvfile2:
    rows = csv.reader(csvfile2)
    for row in rows:
        beall.append(row)
with open('bih_whitelist.csv', newline='', encoding='utf8') as csvfile3:
    rows = csv.reader(csvfile3)
    for row in rows:
        bih.append(row)
with open('history.csv', newline='', encoding='utf8') as csvfile4:
    rows = csv.reader(csvfile4)
    for row in rows:
        history.append(row)
TrainX = np.array(TrainX).astype(np.float)
TrainY = np.array(TrainY)
TrainY = TrainY.ravel()
RFC = RandomForestClassifier(n_estimators=50, random_state=1)
RFC = RFC.fit(TrainX, TrainY)

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def result():
    global RFC, driver, spj, beall
    if request.method == 'POST':
        website = request.values['website']
        driver.get(website)  # 輸入範例網址，交給瀏覽器
        pageSource = driver.page_source  # 取得網頁原始碼
        soup = BeautifulSoup(pageSource, 'lxml')
        pretty = soup.prettify()  # 把網頁內碼編排整齊
        all_text = pretty.split('\n')
        for i in range(len(all_text)):  # 去掉空格
            all_text[i] = all_text[i].strip()
        content = del_tag(all_text)  # 去標籤化
        content_txt = preprocess(content)
        wordvector = convertword(content_txt)
        wordvector = wordvector.astype(np.float)
        predict = RFC.predict(wordvector.reshape(-1,850))
        answer = 'Journal'
        beall_ans = 'Journal'
        spj_ans = 'Journal'
        bih_ans = 'Journal'
        if predict[0] == '0':
            answer = 'Suspected Predatory Journal'
        elif predict[0] == '1':
            answer = 'Normal Journal'
        print(website)
        print(answer)
        setin = []
        setin.append(website)
        setin.append(answer)
        history.append(setin)
        intmp = 0
        if website not in beall[0]:
            beall_ans = 'Not exist on this website'
        else:
            beall_ans = 'Suspected Predatory Journal'
            intmp = 1
        if website not in spj[0]:
            spj_ans = 'Not exist on this website'
        else:
            spj_ans = 'Suspected Predatory Journal'
            intmp = 1
        if website not in bih[0]:
            bih_ans = 'Not exist on this website'
        else:
            bih_ans = 'Normal Journal'
        if intmp == 1:
            answer = 'Suspected Predatory Journal'
        with open('history.csv', 'w', newline='', encoding='utf8') as csvFile:  # 寫入CSV檔
            writer = csv.writer(csvFile)
            writer.writerows(history)
        return render_template('result.html', answer=answer, URL=website, beall=beall_ans, spj=spj_ans, bih=bih_ans)


@app.route('/result', methods=['POST'])
def move_forward():
    if request.method == 'POST':
        return render_template('login.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
