from typing import Any, Dict, List, TypedDict, Union

import pytest


class Currency(TypedDict):
    name: str
    code: str


class OperationAmount(TypedDict):
    amount: str
    currency: Currency


class Transaction(TypedDict):
    id: int
    state: str
    date: str
    operationAmount: OperationAmount
    description: str
    from_: str
    to: str


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


@pytest.fixture
def transaction() -> List[Transaction]:
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from_": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from_": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from_": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод с карты на карту",
            "from_": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from_": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]


@pytest.fixture
def empty_transactions() -> List[Transaction]:
    return []


@pytest.fixture
def single_usd_transaction() -> Transaction:
    return {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from_": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    }
