from typing import List
from src.vacancy import Vacancy


def print_vacancies(vacancies: List[Vacancy]) -> None:
    """Вывод списка вакансий"""
    if not vacancies:
        print("Вакансии не найдены.")
        return

    for i, vacancy in enumerate(vacancies, 1):
        print(f"Вакансия #{i}")
        print(vacancy)


def filter_vacancies(vacancies: List[Vacancy], filter_words: List[str]) -> List[Vacancy]:
    if not filter_words:
        return vacancies

    filtered = []
    for vacancy in vacancies:
        description = vacancy.description.lower() if vacancy.description else ""
        if any(word.lower() in description for word in filter_words):
            filtered.append(vacancy)

    return filtered


def get_vacancies_by_salary(vacancies: List[Vacancy], salary_range: str) -> List[Vacancy]:
    """Фильтрация вакансий по диапазону зарплат"""
    if not salary_range:
        return vacancies

    try:
        min_salary, max_salary = map(int, salary_range.split('-'))
    except ValueError:
        return vacancies

    ranged = []
    for vacancy in vacancies:
        # Получаем значения зарплаты, подставляя 0 если None
        salary_from = vacancy.salary.get('from', 0) or 0
        salary_to = vacancy.salary.get('to', 0) or 0

        # Проверяем попадает ли зарплата в диапазон
        if (salary_from >= min_salary if salary_from else True) and \
                (salary_to <= max_salary if salary_to else True):
            ranged.append(vacancy)

    return ranged


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """Сортировка вакансий по зарплате (по убыванию)"""
    return sorted(vacancies, reverse=True)


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """Получение топ N вакансий"""
    return vacancies[:top_n]
