from typing import List
from datetime import datetime
import pytest
from src.transaction import Transaction
from src.transaction_processor import search_transactions, count_categories


@pytest.fixture
def test_transactions() -> List[Transaction]:
    """
    Создает набор тестовых банковских операций для тестирования.
    """
    return [
        {
            "id": "1",
            "state": "EXECUTED",
            "date": datetime(2019, 8, 26),
            "amount": 100000.0,
            "currency_name": "руб.",
            "currency_code": "RUB",
            "description": "Перевод организации",
            "from_account": "Счет 1234567890123456",
            "to_account": "Счет 0987654321098765"
        },
        {
            "id": "2",
            "state": "EXECUTED",
            "date": datetime(2019, 7, 15),
            "amount": 50000.0,
            "currency_name": "руб.",
            "currency_code": "RUB",
            "description": "Открытие вклада",
            "from_account": "",
            "to_account": "Счет 1234567890123456"
        },
        {
            "id": "3",
            "state": "CANCELED",
            "date": datetime(2019, 6, 30),
            "amount": 30000.0,
            "currency_name": "USD",
            "currency_code": "USD",
            "description": "Перевод с карты на счет",
            "from_account": "Visa 1234 56** **** 7890",
            "to_account": "Счет 0987654321098765"
        }
    ]


class TestSearchTransactions:
    """Набор тестов для функции поиска транзакций по описанию."""

    def test_basic_search(self, test_transactions: List[Transaction]) -> None:
        """
        Проверяет базовый поиск по строке в описании транзакций.
        """
        result = search_transactions(test_transactions, "Перевод")
        assert len(result) == 2
        assert all("перевод" in tr["description"].lower() for tr in result)

    def test_case_insensitive_search(self, test_transactions: List[Transaction]) -> None:
        """
        Проверяет поиск без учета регистра символов.
        """
        variants = ["ПЕРЕВОД", "перевод", "ПеРеВоД"]
        for variant in variants:
            result = search_transactions(test_transactions, variant)
            assert len(result) == 2

    def test_empty_input(self, test_transactions: List[Transaction]) -> None:
        """
        Проверяет обработку пустых входных данных.
        """
        assert search_transactions([], "Перевод") == []
        assert search_transactions(test_transactions, "") == test_transactions


class TestCountCategories:
    """Набор тестов для функции подсчета транзакций по категориям."""

    def test_basic_counting(self, test_transactions: List[Transaction]) -> None:
        """
        Проверяет базовый подсчет количества транзакций по категориям.
        """
        categories = ["Перевод организации", "Открытие вклада", "Перевод с карты на счет"]
        result = count_categories(test_transactions, categories)

        assert result["Перевод организации"] == 1
        assert result["Открытие вклада"] == 1
        assert result["Перевод с карты на счет"] == 1
        assert sum(result.values()) == 3

    def test_missing_categories(self, test_transactions: List[Transaction]) -> None:
        """
        Проверяет обработку отсутствующих категорий.
        """
        categories = ["Несуществующая категория", "Еще одна категория"]
        result = count_categories(test_transactions, categories)

        assert all(count == 0 for count in result.values())
        assert len(result) == len(categories)

    def test_empty_inputs(self, test_transactions: List[Transaction]) -> None:
        """
        Проверяет обработку пустых входных данных.
        """
        assert count_categories([], ["Категория"]) == {"Категория": 0}
        assert count_categories(test_transactions, []) == {}