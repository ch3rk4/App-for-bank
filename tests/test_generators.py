from typing import List, Iterator
#import pytest
from src.generators import filter_by_currency
from tests.conftest import Transaction


def test_filter_by_currency_returns_iterator(empty_transactions: List[Transaction]) -> None:
    """
    Проверяет, что функция возвращает итератор
    """
    result = filter_by_currency(empty_transactions, "USD")
    assert isinstance(result, Iterator)


def test_filter_by_currency_correct_filtering(transaction: List[Transaction]) -> None:
    """
    Проверяет корректность фильтрации транзакций по валюте.
    """
    usd_transactions: List[Transaction] = list(filter_by_currency(transaction, "USD"))

    assert len(usd_transactions) == 3
    assert usd_transactions[0]["operationAmount"]["currency"]["code"] == "USD"
    assert usd_transactions[0]["id"] == 939719570


def test_filter_by_currency_no_matches(transaction: List[Transaction]) -> None:
    """
    Проверяет случай, когда нет транзакций в заданной валюте.
    """
    eur_transactions: List[Transaction] = list(filter_by_currency(transaction, "EUR"))
    assert len(eur_transactions) == 0


def test_filter_by_currency_empty_input(empty_transactions: List[Transaction]) -> None:
    """
    Проверяет обработку пустого списка транзакций.
    """
    result: List[Transaction] = list(filter_by_currency(empty_transactions, "USD"))
    assert len(result) == 0


def test_filter_by_currency_case_sensitivity(transaction: List[Transaction]) -> None:
    """
    Проверяет чувствительность к регистру валюты.
    """
    result: List[Transaction] = list(filter_by_currency(transaction, "usd"))
    assert len(result) == 0


def test_filter_by_currency_preserves_transaction_data(single_usd_transaction: Transaction) -> None:
    """
    Проверяет, что функция сохраняет все данные транзакции.
    """
    usd_transactions: List[Transaction] = list(
        filter_by_currency([single_usd_transaction], "USD")
    )

    expected_keys = {"id", "state", "date", "operationAmount",
                     "description", "from_", "to"}

    assert all(key in usd_transactions[0] for key in expected_keys)
    assert usd_transactions[0]["state"] == "EXECUTED"
    assert usd_transactions[0]["description"] == "Перевод организации"


