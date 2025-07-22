import requests
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class VacancyAPI(ABC):
    """Абстрактный класс для API вакансий"""

    @abstractmethod
    def get_vacancies(self, search_query: str) -> List[Dict[str, Any]]:
        pass


class HeadHunterAPI(VacancyAPI):
    """Класс для работы с API HeadHunter"""

    def __init__(self):
        self.__url = 'https://api.hh.ru/vacancies'
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.__params = {'text': '', 'page': 0, 'per_page': 100, 'area': 113}

    @property
    def url(self) -> str:
        """URL API (только для чтения)"""
        return self.__url

    @property
    def headers(self) -> Dict[str, str]:
        """Заголовки запроса (только для чтения)"""
        return self.__headers

    @property
    def params(self) -> Dict[str, Any]:
        """Параметры запроса (только для чтения)"""
        return self.__params

    def get_vacancies(self, search_query: str) -> List[Dict[str, Any]]:
        """
        Получает вакансии по поисковому запросу
        :param search_query: Поисковый запрос
        :return: Список вакансий
        :raises: Exception при ошибках API
        """
        self.__params['text'] = search_query

        try:
            response = requests.get(
                self.__url,
                headers=self.__headers,
                params=self.__params
            )
            response.raise_for_status()  # Проверка статус-кода

            if response.status_code != 200:
                raise Exception(f"API вернуло статус {response.status_code}")

            return response.json().get('items', [])

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к API: {e}")
            return []
