import pytest
from src.hh_api import HeadHunterAPI


def test_get_vacancies():
    hh_api = HeadHunterAPI()
    vacancies = hh_api.get_vacancies("Python")

    assert isinstance(vacancies, list)
    assert len(vacancies) > 0
    assert 'name' in vacancies[0]
    assert 'alternate_url' in vacancies[0]
