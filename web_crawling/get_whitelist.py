import csv


journal_url = []
with open('whitelist.csv', newline='') as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        journal_url.append(row[8])

with open('url.csv', 'w', newline='', encoding = 'utf8') as csvFile:  # 寫入CSV檔
    writer = csv.writer(csvFile)
    writer.writerow(journal_url)
