import re
from typing import Generator, Iterator, List

from tests.conftest import Transaction


def filter_by_currency(transactions: List[Transaction], cur: str) -> Iterator[Transaction]:
    """
    Функция фильтрует операции по валюте.
    """
    if not cur.isupper():
        return iter([])  # type: ignore
    for transaction in transactions:
        try:
            if transaction["operationAmount"]["currency"]["code"] == cur:
                yield transaction
        except KeyError:
            continue


def transaction_descriptions(transactions: List[Transaction], cur: str) -> Iterator[str]:
    """
     Функция выводит типы валютных операций.
    """
    if not cur.isupper():
        return iter([])  # type: ignore
    for transaction in transactions:
        try:
            if transaction["operationAmount"]["currency"]["code"] == cur:
                yield transaction["description"]
        except KeyError:
            continue


def card_number_generator(start_: str, end_: str) -> Generator[str, None, None]:
    """
    Функция генерирует номер карты
    """
    pattern = r"^\d{4} \d{4} \d{4} \d{4}$"
    if not re.match(pattern, start_) or not re.match(pattern, end_):
        raise ValueError("Номер карты должен быть в формате 'XXXX XXXX XXXX XXXX'")
    current = int(start_.replace(" ", ""))
    end_num = int(end_.replace(" ", ""))
    while current <= end_num:
        card_num = str(current).zfill(16)
        formatted = " ".join([card_num[i : i + 4] for i in range(0, 16, 4)])
        yield formatted
        current += 1
