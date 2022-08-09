import csv
from os import link
import requests
from bs4 import BeautifulSoup


url = 'https://ru.wikipedia.org/wiki/Города_Киргизии#Бывшие_города'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
table = soup.find('div', class_='mw-parser-output').find('table') 


tags = table.findAll('img').find('src')
print(tags)


"""
создание колонок 
"""
head = []
for th in table.find('tr'):
    head.append(' '.join(th.text.split()))

head = head[1:-1:2]
head.append('Ссылка')


"""
Сбор ссылок на города
"""
links = []
for i in table.find_all('tr'):
    for j in i.find_all('a')[0:1]:
        links.append('https://ru.wikipedia.org/' + j.get('href'))
links = links[1:]


"""
Города и информация о них
"""
column = []
for i in table.find_all('tr')[1:]:
    dt = []
    for j in i:
        dt.append(j.text.replace('\n', ''))
    dt = dt[1:-1:2]
    column.append(dt)


""" 
Добавление ссылки к информации о городе
"""
for index, col in enumerate(column):
    col.append(links[index])


""" 
Добавление Заголовок от колонки
"""
column.insert(0, head)


""" 
Сохронение данных в файл CSV
"""
with open('city.csv', 'w') as file:
    writer = csv.writer(file)
    for row in column:
        writer.writerow(row)

