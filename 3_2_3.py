import cProfile
import concurrent
import math
import multiprocessing
import os
import concurrent.futures as pool
import pandas as pd


class DataSet():
    def __init__(self):
        self.folder_name = 'csv'
        file = 'vacancies_by_year.csv'
        self.vacancy = 'Аналитик'
        self.df = pd.read_csv(file)

        self.df['salary'] = self.df[['salary_from', 'salary_to']].mean(axis=1)
        self.df['published_at'] = self.df['published_at'].apply(lambda x: int(x[:4]))
        df_vacancy = self.df[self.df['name'].str.contains(self.vacancy)]
        self.years = self.df['published_at'].unique()
        self.salaryByYears = {year: [] for year in self.years}
        self.vacsByYears = {year: 0 for year in self.years}
        self.vacSalaryByYears = {year: [] for year in self.years}
        self.vacCountByYears = {year: 0 for year in self.years}
        self.GetStaticByCities()
        self.initializeYearStatistics()

    def initializeYearStatistics(self):
        """Добавляет в словари статистик значения из файла
            Также запускает concurrent.futures
        """
        with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
            wait_complete = []
            for task in self.years:
                future = executor.submit(self.getStatisticByYear, task)
                wait_complete.append(future)

        for res in concurrent.futures.as_completed(wait_complete):
            result = res.result()
            year = result[0]
            self.salaryByYears[year] = result[1]
            self.vacsByYears[year] = result[2]
            self.vacSalaryByYears[year] = result[3]
            self.vacCountByYears[year] = result[4]

        self.salaryByYears = dict(sorted(self.salaryByYears.items()))
        self.vacsByYears = dict(sorted(self.vacsByYears.items()))
        self.vacSalaryByYears = dict(sorted(self.vacSalaryByYears.items()))
        self.vacCountByYears = dict(sorted(self.vacCountByYears.items()))
        self.PrintInfo()


    def getStatisticByYear(self, year):
        """Возвращает статистку за год в порядке:
            Среднее значение зарплаты за год,
            Количество вакансий за год.
            Среднее значение зарплаты за год для выбранной профессии.
            Количество вакансий за год для выбранной профессии
        """
        file_path = rf"{self.folder_name}\{year}.csv"
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df["salary"] = df[["salary_from", "salary_to"]].mean(axis=1)
            df_vacancy = df[df["name"].str.contains(self.vacancy)]

            averageSalary = math.floor(df["salary"].mean())
            numberOfVacancies = len(df.index)
            averageSalaryProfession = 0 if df_vacancy.empty else math.floor(df_vacancy["salary"].mean())
            numberOfVacanciesProfession = 0 if df_vacancy.empty else len(df_vacancy.index)

            return [year, averageSalary, numberOfVacancies, averageSalaryProfession,
                                 numberOfVacanciesProfession]

    def PrintInfo(self):
        '''
        Вывод данных
        :return: void
        '''
        print('Динамика уровня зарплат по годам:', self.salaryByYears)
        print('Динамика количества вакансий по годам:', self.vacsByYears)
        print('Динамика уровня зарплат по годам для выбранной профессии:', self.vacSalaryByYears)
        print('Динамика количества вакансий по годам для выбранной профессии:', self.vacCountByYears)
        print('Уровень зарплат по городам (в порядке убывания):', self.salaryArea)
        print('Доля вакансий по городам (в порядке убывания):', self.countArea)

    def GetStaticByCities(self):
        '''
        Получение данных по городам, не требующих multiprocessing
        :return: void
        '''
        total = len(self.df)
        self.df['count'] = self.df.groupby('area_name')['area_name'].transform('count')
        df_norm = self.df[self.df['count'] > 0.01 * total]
        df_area = df_norm.groupby('area_name', as_index=False)['salary'].mean().sort_values(by='salary', ascending=False)
        df_count = df_norm.groupby('area_name', as_index=False)['count'].mean().sort_values(by='count', ascending=False)
        cities = df_count['area_name'].unique()

        self.salaryArea = {city: 0 for city in cities}
        self.countArea = {city: 0 for city in cities}
        for city in cities:
            self.salaryArea[city] = int(df_area[df_area['area_name'] == city]['salary'])
            self.salaryArea = dict(sorted(self.salaryArea.items(), key=lambda x: x[1], reverse=True))
            self.countArea[city] = round(int(df_count[df_count['area_name'] == city]['count']) / total, 4)

if __name__ == '__main__':
    cProfile.run("DataSet()")