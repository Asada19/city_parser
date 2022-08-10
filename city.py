import csv
import requests
from bs4 import BeautifulSoup

def get_url():
    url = 'https://ru.wikipedia.org/wiki/Города_Киргизии#Бывшие_города'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    table = soup.find('div', class_='mw-parser-output').find('table') 
    return table


"""
создание колонок 
"""
def create_head(table):
    head = []
    for th in table.find('tr'):
        head.append(' '.join(th.text.split()))

    head = head[1:-1:2]
    head.append('Ссылка')
    return head


"""
Сбор ссылок на города
"""
links = []

def get_links(links):
    for i in table.find_all('tr'):
        for j in i.find_all('a')[0:1]:
            links.append('https://ru.wikipedia.org/' + j.get('href'))

    links = links[1:]
    return links


"""
Города и информация о них
"""
column = []

def city_data(column: list):
    for i in table.find_all('tr')[1:]:
        dt = []
        for j in i:
            dt.append(j.text.replace('\n', ''))
        dt = dt[1:-1:2]
        column.append(dt)


""" 
Добавление ссылки к информации о городе
"""
def add_links(links, column):
    for index, col in enumerate(column):
        col.append(links[index])


"""     
Добавление Заголовок от колонки
"""
def form_data(header, column):
    header.remove('Флаг, герб')
    for i in column:
        for x in i:
            if x == ' ':             
                i.remove(x)
            elif x == '':
                i.remove(x)

    column.insert(0, header)
    return column


""" 
Сохронение данных в файл CSV
"""
def write_to_csv(data):
    with open('city.csv', 'w') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)



table = get_url()
header = create_head(table)
get_links(links)
city_data(column)
add_links(links, column)
data = form_data(header, column)
write_to_csv(data)
