import pandas as pd
import math

# Задаем основные настройки и считываем файлы
pd.set_option("display.max_columns", None)
df_currencies = pd.read_csv("currencies.csv")
data = {"name": [], "salary": [], "area_name": [], "published_at": []}
currency = ['RUR', 'USD', 'KZT', 'BYR', 'UAH', 'EUR']
df = pd.read_csv("vacancies_dif_currencies.csv")

# Основной цикл, перебираем весь файл
for index, row in df.iterrows():
    # для создания файла на 100 строк
    if len(data['name']) >= 100:
        break
    # выделяем основные переменные
    salary_from = row["salary_from"]
    salary_to = row["salary_to"]
    value_curr = row["salary_currency"]
    # данные, не требующие обработки
    if math.isnan(salary_from) and math.isnan(salary_to):
        continue
    if value_curr not in currency:
        continue
    # Получаем коэффициент для перевода в ррубли
    if value_curr != 'RUR':
        date = row["published_at"]
        date = date[:7]
        k = float(df_currencies[df_currencies["date"] == date][value_curr].values)
    else:
        k = 1
    if math.isnan(salary_from) or math.isnan(salary_to):
        if math.isnan(salary_from):
            data["salary"].append(salary_to * k)
        else:
            data["salary"].append(salary_from * k)
    else:
        data["salary"].append(((salary_from + salary_to) / 2) * k)

    # Заполняем данные
    data["name"].append(row["name"])
    data["area_name"].append(row["area_name"])
    data["published_at"].append(row["published_at"])

# Сохраняем в csv
new_df = pd.DataFrame(data)
new_df.to_csv("vacancies.csv")