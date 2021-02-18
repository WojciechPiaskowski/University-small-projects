from pymongo import MongoClient
import requests
import lxml.html as lh
import pandas as pd

Client = MongoClient('mongodb://localhost:27017')
database = Client['db_WojciechP']
sites = ['http://www.bankier.pl/gielda/notowania/akcje', 'http://finance.yahoo.com/most-active']

data = database.stocksWojciechP

for site in sites:
    print('Scraping site: ', site)
    html = requests.get(site).text
    doc = {'url':site,
           'html':html}
    data.insert_one(doc)
    print('Data uploaded: ', data.find_one({'url':site}), '\n')

data2 = database.stocksWojciechP2

website = lh.fromstring(data.find_one({'url':sites[0]})['html'])
table = website.xpath('//tr')
table2 = []

for i in table:
    if len(i) != 10:
        continue
    else:
        table2.append(i)

table = table2

col=[]
i=0

for t in table[0]:
    i += 1
    name = t.text_content()
    print ('%d:"%s"'%(i,name))
    col.append((name,[]))


for j in range(1, len(table)):
    # T is our j'th row
    T = table[j]

    i = 0


    for t in T.iterchildren():
        element = t.text_content()

        if i > 0:

            try:
                element = float(element)
            except:
                pass

        col[i][1].append(element)
        # Increment i for the next column
        i += 1

Dict={title:column for (title,column) in col}

df = pd.DataFrame(Dict)

df.iloc[:,0] = df.iloc[:,0].str.strip()

for index, row in df.iterrows():
    print('Adding... ', row['Walor AD'])

    document = {
        'Walor':str(row['Walor AD']),
        'Kurs': str(row['Kurs AD']),
        'Zmiana': str(row['Zmiana AD']),
        'Zmianaprocentowa': str(row['Zmianaprocentowa AD']),
        'Liczbatransakcji': str(row['Liczbatransakcji AD']),
        'Otwarcie': str(row['Otwarcie AD']),
        'Max': str(row['Max AD']),
        'Min': str(row['Min AD']),
        'Czas': str(row['Czas AD']),
    }

    data2.insert_one(document)

for i in data2.find():
    print(i['Walor'], i['Kurs'], i['Zmiana'], '\n')

for i in data2.find():
    print(i, '\n', '***************************************************', '\n')


