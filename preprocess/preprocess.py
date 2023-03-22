import csv
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
from nltk.stem import WordNetLemmatizer
import sys


lemmatizer = WordNetLemmatizer()
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

maxInt = sys.maxsize
while True:
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)
punc = ['!', '?', ',', ':', '"', '(', ')', '<', '>', '{', '}', '=', '@', '#', '$', '%', '/', '[', ']', '^', '_', '|', '+', '-', '*', ';', '~', '&', '©', '–', '”', '“', '…', '—', '→', '.', '’'] # 特殊符號集
pj_content = []
goodj_content = []
with open('blacklist_dataset.csv', newline='', encoding='utf8') as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        pj_content.append(row)
with open('whitelist_dataset.csv', newline='', encoding='utf8') as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        goodj_content.append(row)

good = []
bad = []
all_journal = []
stopword = stopwords.words('english')  # 停用詞
p = re.compile('[^a-z^A-Z^0-9^.]')  # 英文跟數字的正規化
for w in punc:
    stopword.append(w)  # 把標點符號加入停用詞
for pj_no in range(len(pj_content)):  # pj_no為第幾個網頁內容
    word = []
    content_text = []  # 內容每一行裡的單字
    for text in pj_content[pj_no]:  # 內容裡每行的句子
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
                                #print(wo)
                                content_text.append(wo)
    if content_text != '':
        bad.append(content_text)
        all_journal.append(content_text)
print(bad)

for gj_no in range(len(goodj_content)):  # pj_no為第幾個網頁內容
    word = []
    content_text = []  # 內容每一行裡的單字
    for text in goodj_content[gj_no]:  # 內容裡每行的句子
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
                                #print(wo)
                                content_text.append(wo)
    if content_text != '':
        good.append(content_text)
        all_journal.append(content_text)
print(good)


with open('pj_content.csv', 'w', newline='', encoding = 'utf8') as csvFile2:  # 寫入CSV檔
    writer = csv.writer(csvFile2)
    writer.writerows(bad)

with open('goodj_content.csv', 'w', newline='', encoding = 'utf8') as csvFile3:  # 寫入CSV檔
    writer = csv.writer(csvFile3)
    writer.writerows(good)

with open('allj_content.csv', 'w', newline='', encoding = 'utf8') as csvFile4:  # 寫入CSV檔
    writer = csv.writer(csvFile4)
    writer.writerows(all_journal)







