import json
from typing import List, Dict, Any
from src.abstract_classes import Saver
from src.vacancy import Vacancy


class JSONSaver(Saver):
    """Класс для сохранения вакансий в JSON-файл"""

    def __init__(self, filename: str = 'data/vacancies.json'):
        """
        :param filename: Путь к JSON-файлу (по умолчанию: data/vacancies.json)
        """
        self.__filename = filename  # Делаем атрибут приватным

    @property
    def filename(self) -> str:
        """Возвращает путь к файлу (только для чтения)"""
        return self.__filename

    def add_vacancy(self, vacancy) -> None:
        """
        Добавляет вакансию в файл, если она отсутствует
        :param vacancy: Объект вакансии
        """
        vacancies = self._load_vacancies()

        # Создаем словарь вручную, так как __slots__ запрещает __dict__
        vacancy_data = {
            'title': vacancy.title,
            'url': vacancy.url,
            'salary': vacancy.salary,
            'description': vacancy.description
        }

        # Проверяем дубликаты по URL и названию
        if not any(
                v['url'] == vacancy.url and v['title'] == vacancy.title
                for v in vacancies
        ):
            vacancies.append(vacancy_data)
            self._save_vacancies(vacancies)

    def delete_vacancy(self, vacancy) -> None:
        """
        Удаляет вакансию из файла
        :param vacancy: Объект вакансии для удаления
        """
        vacancies = self._load_vacancies()
        vacancies = [
            v for v in vacancies
            if not (v['url'] == vacancy.url and v['title'] == vacancy.title)
        ]
        self._save_vacancies(vacancies)

    def get_vacancies_by_criteria(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Получение вакансий по критериям"""
        vacancies = self._load_vacancies()
        filtered_vacancies = []

        for vacancy in vacancies:
            match = True
            for key, value in criteria.items():
                if key == 'salary_from':
                    if vacancy['salary'].get('from', 0) < value:
                        match = False
                elif key == 'salary_to':
                    if vacancy['salary'].get('to', float('inf')) > value:
                        match = False
                elif key == 'keyword':
                    if value.lower() not in vacancy['description'].lower():
                        match = False
                elif vacancy.get(key) != value:
                    match = False

            if match:
                filtered_vacancies.append(vacancy)

        return filtered_vacancies

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаление вакансии из файла"""
        vacancies = self._load_vacancies()
        vacancies = [v for v in vacancies if v['url'] != vacancy.url]
        self._save_vacancies(vacancies)

    def _load_vacancies(self) -> List[Dict[str, Any]]:
        try:
            with open(self.__filename, 'r', encoding='utf-8') as file:  # Исправлено
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_vacancies(self, vacancies: List[Dict[str, Any]]) -> None:
        with open(self.__filename, 'w', encoding='utf-8') as file:  # Исправлено
            json.dump(vacancies, file, ensure_ascii=False, indent=2)
