from typing import Dict, Any, List


class Vacancy:
    """Класс для представления вакансии"""

    __slots__ = ['title', 'url', 'salary', 'description']  # Оптимизация памяти

    def __init__(self, title: str, url: str, salary: Dict[str, Any], description: str):
        self.__validate_salary(salary)  # Валидация данных

        self.title = title
        self.url = url
        self.salary = salary or {'from': None, 'to': None, 'currency': None}
        self.description = description or "Описание не указано"

    def __validate_salary(self, salary: Dict[str, Any]) -> None:
        """Приватный метод валидации структуры зарплаты"""
        if salary is not None and not isinstance(salary, dict):
            raise ValueError("Зарплата должна быть словарём или None")

        if salary:
            valid_keys = {'from', 'to', 'currency', 'gross'}
            if not all(key in valid_keys for key in salary.keys()):
                raise ValueError("Некорректные ключи в данных о зарплате")

    def __str__(self):
        salary_from = self.salary.get('from', 'не указана')
        salary_to = self.salary.get('to', 'не указана')
        currency = self.salary.get('currency', '')
        return (f"Вакансия: {self.title}\n"
                f"Зарплата: от {salary_from} до {salary_to} {currency}\n"
                f"Описание: {self.description[:100]}...\n"
                f"Ссылка: {self.url}\n")

    def __lt__(self, other):
        """Сравнение вакансий по зарплате (меньше)"""
        return self.get_average_salary() < other.get_average_salary()

    def __gt__(self, other):
        """Сравнение вакансий по зарплате (больше)"""
        return self.get_average_salary() > other.get_average_salary()

    def get_average_salary(self) -> int:
        """Вычисление средней зарплаты для сравнения"""
        salary_from = self.salary.get('from') or 0
        salary_to = self.salary.get('to') or 0

        if salary_from and salary_to:
            return (salary_from + salary_to) // 2
        elif salary_from:
            return salary_from
        elif salary_to:
            return salary_to
        return 0

    @classmethod
    def cast_to_object_list(cls, vacancies_data: List[Dict[str, Any]]) -> List['Vacancy']:
        vacancies = []
        for item in vacancies_data:
            title = item.get('name', 'Без названия')
            url = item.get('alternate_url', 'Ссылка не указана')
            salary = item.get('salary')
            description = item.get('snippet', {}).get('requirement', 'Описание не указано')

            vacancies.append(cls(title, url, salary, description))

        return vacancies
