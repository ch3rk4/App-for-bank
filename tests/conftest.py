from typing import Any, Dict, List, Union

import pytest


@pytest.fixture
def numbers_1() -> str:
    return "7000 79** **** 6361"


@pytest.fixture
def numbers_2() -> str:
    return "**4305"


@pytest.fixture
def error_() -> str:
    return "Ошибка ввода"


@pytest.fixture
def card_1() -> str:
    return "Visa Platinum 7000 79** **** 6361"


@pytest.fixture
def card_2() -> str:
    return "Maestro 7000 79** **** 6361"


@pytest.fixture
def account_1() -> str:
    return "Счет **4305"


@pytest.fixture
def date_() -> str:
    return "11.03.2024"


@pytest.fixture
def valid_operations() -> List[Dict[str, Any]]:
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture
def invalid_operations() -> List[Union[Dict[str, Any], str]]:
    return [{"id": 41428829, "state": "EXECUTED"}, "not_a_dict"]


@pytest.fixture
def invalid_date_operations() -> List[Dict[str, Any]]:
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "invalid_date"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]


@pytest.fixture
def no_date_operations() -> List[Dict[str, Any]]:
    return [
        {"id": 41428829, "state": "EXECUTED"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]
