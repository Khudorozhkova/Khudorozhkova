from datetime import datetime

import pandas as pd

'''
Ссылка на файл и создание датафрейма
'''
file = 'vacancies_by_year.csv'
vacancy = 'Аналитик'
df = pd.read_csv(file)

df['salary'] = df[['salary_from', 'salary_to']].mean(axis=1)
df['published_at'] = df['published_at'].apply(lambda x: int(x[:4]))
df_vacancy = df[df['name'].str.contains(vacancy)]
years = df['published_at'].unique()

salary_by_years = {year: [] for year in years}
vacs_by_years = {year: 0 for year in years}
vac_salary_by_years = {year: [] for year in years}
vac_count_by_years = {year: 0 for year in years}

for year in years:
    salary_by_years[year] = int(df[df['published_at'] == year]['salary'].mean())
    vacs_by_years[year] = len(df[df['published_at'] == year])
    vac_salary_by_years[year] = int(df_vacancy[df_vacancy['published_at'] == year]['salary'].mean())
    vac_count_by_years[year] = len(df_vacancy[df_vacancy['published_at'] == year].index)

print('Динамика уровня зарплат по годам:', salary_by_years)
print('Динамика количества вакансий по годам:', vacs_by_years)
print('Динамика уровня зарплат по годам для выбранной профессии:', vac_salary_by_years)
print('Динамика количества вакансий по годам для выбранной профессии:', vac_count_by_years)


total = len(df)
df['count'] = df.groupby('area_name')['area_name'].transform('count')
df_norm = df[df['count'] > 0.01 * total]
df_area = df_norm.groupby('area_name', as_index=False)['salary'].mean().sort_values(by='salary', ascending=False)
print(df_area)
df_count = df_norm.groupby('area_name', as_index=False)['count'].mean().sort_values(by='count', ascending=False)
print(df_count)