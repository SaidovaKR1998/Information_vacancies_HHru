from src.vacancy import Vacancy


def test_vacancy_creation():
    vacancy = Vacancy(
        title="Python Developer",
        url="https://hh.ru/vacancy/123",
        salary={'from': 100000, 'to': 150000, 'currency': 'RUR'},
        description="Требуется Python разработчик"
    )

    assert vacancy.title == "Python Developer"
    assert vacancy.url == "https://hh.ru/vacancy/123"
    assert vacancy.salary['from'] == 100000
    assert vacancy.description.startswith("Требуется")


def test_vacancy_comparison():
    vacancy1 = Vacancy("Junior", "url1", {'from': 50000}, "desc1")
    vacancy2 = Vacancy("Middle", "url2", {'from': 100000}, "desc2")

    assert vacancy1 < vacancy2
    assert vacancy2 > vacancy1


def test_cast_to_object_list():
    data = [{
        'name': 'Python Dev',
        'alternate_url': 'https://hh.ru/vacancy/123',
        'salary': {'from': 100000, 'to': 150000, 'currency': 'RUR'},
        'snippet': {'requirement': 'Опыт работы 3 года'}
    }]

    vacancies = Vacancy.cast_to_object_list(data)
    assert len(vacancies) == 1
    assert isinstance(vacancies[0], Vacancy)
    assert vacancies[0].title == "Python Dev"
