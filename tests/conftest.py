import pytest


@pytest.fixture
def numbers_1():
    return "7000 79** **** 6361"


@pytest.fixture
def numbers_2():
    return "**4305"


@pytest.fixture
def error_():
    return "Ошибка ввода"


@pytest.fixture
def card_1():
    return "Visa Platinum 7000 79** **** 6361"


@pytest.fixture
def card_2():
    return "Maestro 7000 79** **** 6361"


@pytest.fixture
def account_1():
    return "Счет **4305"


@pytest.fixture
def date_():
    return "11.03.2024"


@pytest.fixture
def sample_operations():
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]
