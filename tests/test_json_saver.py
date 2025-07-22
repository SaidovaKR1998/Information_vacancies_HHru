import pytest
import os
import json
from src.json_saver import JSONSaver
from src.vacancy import Vacancy

TEST_FILE = 'test_vacancies.json'


@pytest.fixture
def clean_test_file():
    """Фикстура для очистки тестового файла перед каждым тестом"""
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    yield
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)


@pytest.fixture
def sample_vacancy():
    """Фикстура с примером вакансии"""
    return Vacancy(
        title="Python Developer",
        url="https://hh.ru/vacancy/123",
        salary={'from': 100000, 'to': 150000, 'currency': 'RUR'},
        description="Требуется опыт работы 3+ года"
    )


def test_json_saver_initialization():
    """Тест инициализации JSONSaver"""
    saver = JSONSaver(TEST_FILE)
    assert saver.filename == TEST_FILE
    with pytest.raises(AttributeError):
        saver.__filename


def test_add_and_load_vacancies(clean_test_file, sample_vacancy):
    """Тест добавления и загрузки вакансий"""
    saver = JSONSaver(TEST_FILE)

    # Добавляем вакансию
    saver.add_vacancy(sample_vacancy)

    # Проверяем загрузку
    loaded = saver.get_vacancies_by_criteria({})
    assert len(loaded) == 1
    assert loaded[0]['title'] == sample_vacancy.title
    assert loaded[0]['url'] == sample_vacancy.url


def test_no_duplicate_vacancies(clean_test_file, sample_vacancy):
    """Тест отсутствия дубликатов"""
    saver = JSONSaver(TEST_FILE)

    # Первое добавление
    saver.add_vacancy(sample_vacancy)
    assert len(saver.get_vacancies_by_criteria({})) == 1

    # Пытаемся добавить дубликат
    saver.add_vacancy(sample_vacancy)
    assert len(saver.get_vacancies_by_criteria({})) == 1


def test_delete_vacancy(clean_test_file, sample_vacancy):
    """Тест удаления вакансии"""
    saver = JSONSaver(TEST_FILE)
    saver.add_vacancy(sample_vacancy)
    assert len(saver.get_vacancies_by_criteria({})) == 1

    saver.delete_vacancy(sample_vacancy)
    assert len(saver.get_vacancies_by_criteria({})) == 0


def test_get_vacancies_by_criteria(clean_test_file, sample_vacancy):
    """Тест фильтрации вакансий"""
    saver = JSONSaver(TEST_FILE)
    saver.add_vacancy(sample_vacancy)

    # Поиск по существующему ключевому слову
    results = saver.get_vacancies_by_criteria({'keyword': 'опыт'})
    assert len(results) == 1

    # Поиск по несуществующему критерию
    results = saver.get_vacancies_by_criteria({'keyword': 'javascript'})
    assert len(results) == 0


def test_default_filename():
    """Тест имени файла по умолчанию"""
    saver = JSONSaver()
    assert saver.filename == 'data/vacancies.json'
