from datetime import datetime

import pandas as pd

'''Ссылка на файл и создание датафрейма'''
file = 'vacancies_by_year.csv'
df = pd.read_csv(file)

'''Создаем новую колонку'''
df['years'] = df['published_at'].apply(lambda s: datetime.strptime(s, '%Y-%m-%dT%H:%M:%S%z').year)
# print(df.head(10))

years = df['years'].unique()

'''Заполняем csv файлы'''
for year in years:
    data = df[df['years'] == year]
    data.iloc[:, :6].to_csv(rf'csv\{year}.csv', index=False)