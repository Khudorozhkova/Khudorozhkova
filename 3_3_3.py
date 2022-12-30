from datetime import datetime
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from dateutil import rrule
import pandas as pd
import requests
import json

# задаем основные настройки и переменные
pd.set_option("display.max_columns", None)
data = {'name': [], 'salary_from': [], 'salary_to': [], 'salary_currency': [], 'area_name': [], 'published_at': []}
date = ['2022-12-23T00:00:00', '2022-12-23T06:00:00', '2022-12-23T12:00:00', '2022-12-23T18:00:00', '2022-12-24T00:00:00']

# цикл для прохода по часам
for k in range(len(date) - 1):
    date_from = date[k]
    date_to = date[k+1]
    # проходимся по страницам
    for j in range(1, 20):
        # данные с запроса
        request = requests.get(
            f'https://api.hh.ru/vacancies?date_from={date_from}&date_to={date_to}&specialization=1&per_page=100&page={j}')
        jsonText = request.text
        jsonData = json.loads(jsonText)
        a = 1
        items = jsonData['items']
        # не делаем лишних запросов, если данные за промежуток кончились
        if len(items) == 0:
            break
        # сохраняем данные из запроса
        for i in items:
            data['name'].append(i['name'])
            salary = i['salary']
            if salary != None:
                data['salary_from'].append(salary['from'])
                data['salary_to'].append(salary['to'])
                data['salary_currency'].append(salary['currency'])
            else:
                data['salary_from'].append(None)
                data['salary_to'].append(None)
                data['salary_currency'].append(None)
            area = i['area']
            if area != None:
                data['area_name'].append(area['name'])
            else:
                data['area_name'].append(None)
            data['published_at'].append(i['published_at'])

# сохраняем в csv
df = pd.DataFrame(data)
df.to_csv('hh.csv')