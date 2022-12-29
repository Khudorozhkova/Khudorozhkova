from unittest import TestCase, main
from code_Fail import Salary
from code_Fail import DataSet
import unittest


class Test2(TestCase):

    def test_SalaryTypeTest(self):
        self.assertEqual(type(Salary(dic={"salary_from" : 100, "salary_to" : 200, "salary_currency" : "RUR"})).__name__, 'Salary')  # add assertion here
    def test_AveregeSalaryTest(self):
        self.assertEqual(Salary(dic={"salary_from" : 100, "salary_to" : 200, "salary_currency" : "RUR"}).averageSalary, 150.0)
    def test_SalaryCurrencyTest(self):
        self.assertEqual(Salary(dic={"salary_from" : 100, "salary_to" : 200, "salary_currency" : "EUR"}).salaryRub, 8985.0)
    def test_TryToAddTest(self):
        self.assertEqual(DataSet().tryToAdd(dic={'1' : 1}, key='1', val=1), {'1': 2})
        self.assertEqual(DataSet().tryToAdd(dic={'1' : 1}, key='2', val=2), {'1': 1, '2': 2})
    def test_DatasetAveregeSalaryTest(self):
        self.assertEqual(DataSet().getAverageSalary(count={'2007': 2}, sum={'2007': 10}), {'2007': 5})
    def test_SortedDictTest(self):
        self.assertEqual(len(DataSet().getSortedDict(
            keySalary={'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, '11': 11,
                       '12': 12})), 10)
    def test_UpdateKeysTest(self):
        self.assertEqual(DataSet().updateKeys(keyCount={'2022': 1000}),
            {'2022': 1000, 2007: 0, 2008: 0, 2009: 0, 2010: 0, 2011: 0, 2012: 0, 2013: 0, 2014: 0, 2015: 0, 2016: 0, 2017: 0, 2018: 0, 2019: 0, 2020: 0, 2021: 0, 2022: 0})
        self.assertEqual(DataSet().updateKeys(keyCount={'2023' : 1000}),
            {'2023': 1000, 2007: 0, 2008: 0, 2009: 0, 2010: 0, 2011: 0, 2012: 0, 2013: 0, 2014: 0, 2015: 0, 2016: 0, 2017: 0, 2018: 0, 2019: 0, 2020: 0, 2021: 0, 2022: 0})

if __name__ == '__main__':
    main()