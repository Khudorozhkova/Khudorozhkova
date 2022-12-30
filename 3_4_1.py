import pandas as pd
import math

# Задаем основные настройки и считываем файлы
pd.set_option("display.max_columns", None)
df_currencies = pd.read_csv("currencies.csv")
data = {"name": [], "salary": [], "area_name": [], "published_at": []}
currency = ['RUR', 'USD', 'KZT', 'BYR', 'UAH', 'EUR']
df = pd.read_csv("vacancies_dif_currencies.csv")

# Получаем название вакансии
def GetName(row):
    return row['name']

# получаем город вакансии
def GetAreaName(row):
    return row['area_name']

# Получаем дату публикации
def GetPublished(row):
    return row['published_at']

def GetSalary(row):
    # выделяем основные переменные
    salary_from = row["salary_from"]
    salary_to = row["salary_to"]
    value_curr = row["salary_currency"]
    # данные, не требующие обработки
    if math.isnan(salary_from) and math.isnan(salary_to):
        return None
    if value_curr not in currency:
        return None
    # Получаем коэффициент для перевода в ррубли
    if value_curr != 'RUR':
        date = row["published_at"]
        date = date[:7]
        k2 = df_currencies[df_currencies["date"] == date]
        k3 = k2[value_curr].values
        # Применяем try except, тк есть пропуски в данных df_currencies
        try:
            k = float(k3)
        except:
            k = 0
    # Получение зарплаты
    else:
        k = 1
    if math.isnan(salary_from) or math.isnan(salary_to):
        if math.isnan(salary_from):
            salary = salary_to * k
        else:
            salary = salary_from * k
    else:
        salary = ((salary_from + salary_to) / 2) * k
    return salary

# Заполняем новый дата фрейм
new_df = pd.DataFrame(data)
new_df['name'] = df['name']
new_df['area_name'] = df['area_name']
new_df['published_at'] = df['published_at']
# Вместо цикла используем apply
new_df['salary'] = df.apply(GetSalary, axis=1)

# Сохраняем в csv
df_to_csv = new_df.head(100)
df_to_csv.to_csv("vacancies2.csv")