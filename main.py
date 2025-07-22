from src.hh_api import HeadHunterAPI
from src.vacancy import Vacancy
from src.json_saver import JSONSaver
from src.file_savers import CSVSaver, ExcelSaver
from src.user_interaction import (print_vacancies, filter_vacancies,
                                  get_vacancies_by_salary, sort_vacancies,
                                  get_top_vacancies)


def user_interaction():
    """Функция для взаимодействия с пользователем"""
    hh_api = HeadHunterAPI()
    json_saver = JSONSaver()

    print("Добро пожаловать в программу для поиска вакансий!")
    search_query = input("Введите поисковый запрос (например, Python): ")

    # Получение вакансий с hh.ru
    print("\nПолучаем вакансии с hh.ru...")
    hh_vacancies = hh_api.get_vacancies(search_query)
    vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)

    # Сохранение вакансий в файл
    for vacancy in vacancies_list:
        json_saver.add_vacancy(vacancy)

    # Фильтрация и сортировка
    top_n = int(input("\nВведите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий (через пробел): ").split()
    salary_range = input("Введите диапазон зарплат (например: 100000-150000): ")

    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
    sorted_vacancies = sort_vacancies(ranged_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    # Вывод результатов
    print("\nРезультаты поиска:")
    print_vacancies(top_vacancies)


if __name__ == "__main__":
    user_interaction()
