from datetime import datetime
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from dateutil import rrule
import pandas as pd

'''
RUR    1830967
USD     167994
KZT      65291
BYR      41178
UAH      25969
EUR      10641
'''
currency = ['USD', 'KZT', 'BYR', 'UAH', 'EUR']
pd.set_option("display.max_columns", None)
file = "vacancies_dif_currencies.csv"
df = pd.read_csv(file)

print(df.head())

minDate = df['published_at'].min()
maxDate = df['published_at'].max()
minDate = datetime.strptime(minDate, '%Y-%m-%dT%H:%M:%S%z')
maxDate = datetime.strptime(maxDate, '%Y-%m-%dT%H:%M:%S%z')
print(type(maxDate))

result = {'date' : [], 'USD': [], 'KZT' : [], 'BYR' : [],  'UAH' : [], 'EUR' : []}

# Цикл для прохождения по каждому месяцу с 2003 по 2022
for dt in rrule.rrule(rrule.MONTHLY, dtstart=minDate, until=maxDate):
    # Дерево для чтения xml (А хочется json...)
    tree = ET.parse(
        # urlopen(f'http://www.cbr.ru/scripts/XML_daily.asp?date_reg=28/{dt.strftime("%m/%Y")}d=1')
        urlopen(f'https://www.cbr.ru/scripts/XML_daily.asp?date_req=28/{dt.strftime("%m/%Y")}d=1')
    )
    root = tree.getroot()
    # Проходимся по дереву в цикле
    for child in root.findall('Valute'):
        code = child.find('CharCode').text
        a = result.keys()
        # Получаем нужные значения
        if code in result.keys():
            if dt.strftime('%Y-%m') not in result['date']:
                result['date'] += [dt.strftime('%Y-%m')]
            k = float(child.find('Value').text.replace(',', '.')) / float(child.find('Nominal').text)
            result[code].append(k)
            print(code == 'BYR')
    # Заполняем пустые значения BYR
    if len(result['BYR']) != len(result['date']):
        result['BYR'].append(None)
new_df = pd.DataFrame(result)
new_df.to_csv('currencies.csv')
print(new_df.head())
