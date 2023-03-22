import csv


punc = ['!', '?', ',', ':', '"', '(', ')', '<', '>', '{', '}', '=', '@', '#', '$', '%', '/', '[', ']', '^', '_', '|', '+', '-', '*', ';', '~', '&', '©', '–', '”', '“', '…', '—', '→'] # 兔舒服號及
pj_content = []
with open('dataset.csv', newline='', encoding='utf8') as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        pj_content.append(row)
        #print(row)
BOW = []  # 詞袋list
pj_word = []
for pj_no in range(len(pj_content)):  # pj_no為第幾個網頁內容
    word = []
    content_text = []  # 內容每一行裡的句子
    for text in pj_content[pj_no]:  # 把句子用空格來切割出來 因此能得到每個單字
        text_seperate = text.split()
        for w in text_seperate:
            if w != '':
                content_text.append(w)
    for i in range(len(content_text)):  # 依據每個單字去做判斷是否有特殊符號
        if content_text[i] == '[...]':
            content_text[i] = ''
        elif content_text[i].isalnum():  # 把單字裡的英文字母都改為小寫
            content_text[i] = content_text[i].lower()
            if content_text[i] not in BOW:
                BOW.append(content_text[i])  # 如果此單詞沒有在BOW中 把只有純單字或數字給轉成小寫英文 並加入到詞袋(BOW)中
            word.append((content_text[i]))
        else:  # 如果裡面有特殊符號
            length = len(content_text[i])
            while True:  # 把最後結尾的.給去掉
                if length == 0:
                    break
                elif content_text[i][0] == '.':
                    content_text[i] = content_text[i][1:length]
                    length = len(content_text[i])
                elif content_text[i][length-1] == '.':
                    content_text[i] = content_text[i][:length-1]
                    length = len(content_text[i])
                else:
                    break
            length = len(content_text[i])
            for j in range(length):  # 把特殊符號用空格來取代
                if content_text[i][j] in punc:
                    content_text[i] = content_text[i][:j] + ' ' + content_text[i][j+1:]
            get_text = content_text[i].split()  # 利用剛剛的空格來切割字詞
            for space in get_text:
                if space != '':
                    length = len(space)
                    if space[length - 1] == '.':  # 把字詞結尾的.給去掉
                        space = space[:length-1]
                    space = space.strip()
                    space = space.lower()
                    if space not in BOW:
                        BOW.append(space)  # 把處理好的字詞加入到詞袋(BOW)中
                    word.append(space)
                    #print(space)
    pj_word.append(word)

with open('BOW.csv', 'w', newline='', encoding = 'utf8') as csvFile:  # 寫入CSV檔
    writer = csv.writer(csvFile)
    writer.writerow(BOW)

with open('pj_content.csv', 'w', newline='', encoding = 'utf8') as csvFile2:  # 寫入CSV檔
    writer = csv.writer(csvFile2)
    writer.writerows(pj_word)





