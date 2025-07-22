from abc import ABC, abstractmethod
import json


class VacancyAPI(ABC):
    """Абстрактный класс для работы с API сервиса с вакансиями"""

    @abstractmethod
    def get_vacancies(self, search_query):
        pass


class Saver(ABC):
    """Абстрактный класс для сохранения вакансий"""

    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies_by_criteria(self, criteria):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        pass
