from typing import List
import pytest
from src.transaction_processor import Transaction, search_transactions, count_categories


@pytest.fixture
def test_transactions() -> List[Transaction]:
    """
    Создает набор тестовых транзакций разных типов для тестирования.
    """
    return [
        {
            "id": 1,
            "description": "Перевод организации",
            "status": "EXECUTED",
            "amount": 100000.0,
            "currency": "RUB"
        },
        {
            "id": 2,
            "description": "Открытие вклада",
            "status": "EXECUTED",
            "amount": 50000.0,
            "currency": "RUB"
        },
        {
            "id": 3,
            "description": "Перевод с карты на счет",
            "status": "CANCELED",
            "amount": 30000.0,
            "currency": "USD"
        },
        {
            "id": 4,
            "description": "ПЕРЕВОД организации",
            "status": "PENDING",
            "amount": 20000.0,
            "currency": "EUR"
        },
        {
            "id": 5,
            "description": None,
            "status": "EXECUTED",
            "amount": 10000.0,
            "currency": "RUB"
        }
    ]


class TestSearchTransactions:
    """Набор тестов для функции поиска транзакций по описанию."""

    def test_basic_search(self, test_transactions: List[Transaction]) -> None:
        """
        Проверяет базовый поиск по строке в описании транзакций.
        """
        result = search_transactions(test_transactions, "Перевод")
        assert len(result) == 3
        assert all(
            tr["description"] is not None and "перевод" in tr["description"].lower()
            for tr in result
        )

    def test_case_insensitive_search(self, test_transactions: List[Transaction]) -> None:
        """
        Проверяет поиск без учета регистра символов.
        """
        variants = ["ПЕРЕВОД", "перевод", "ПеРеВоД"]
        for variant in variants:
            result = search_transactions(test_transactions, variant)
            assert len(result) == 3

    def test_partial_match(self, test_transactions: List[Transaction]) -> None:
        """
        Проверяет поиск по частичному совпадению строки.
        """
        assert len(search_transactions(test_transactions, "орг")) == 2
        assert len(search_transactions(test_transactions, "карт")) == 1

    def test_exact_match(self, test_transactions: List[Transaction]) -> None:
        """
        Проверяет поиск по точному совпадению строки.
        """
        result = search_transactions(test_transactions, "Открытие вклада")
        assert len(result) == 1
        assert result[0]["description"] == "Открытие вклада"

    def test_no_match(self, test_transactions: List[Transaction]) -> None:
        """
        Проверяет случай, когда совпадения не найдены.
        """
        result = search_transactions(test_transactions, "несуществующий")
        assert len(result) == 0

    def test_empty_input(self, test_transactions: List[Transaction]) -> None:
        """
        Проверяет обработку пустых входных данных.
        """
        assert search_transactions([], "Перевод") == []
        assert search_transactions(test_transactions, "") == test_transactions

    def test_special_characters(self, test_transactions: List[Transaction]) -> None:
        """
        Проверяет обработку специальных символов в строке поиска.
        """
        special_chars = [".*", "?", "[", "]", "\\"]
        for char in special_chars:
            assert len(search_transactions(test_transactions, char)) == 0

    def test_none_description(self, test_transactions: List[Transaction]) -> None:
        """
        Проверяет обработку транзакций с пустым описанием (None).
        """
        result = search_transactions(test_transactions, "любой текст")
        assert all(tr["description"] is not None for tr in result)


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

    def test_case_sensitive_counting(self, test_transactions: List[Transaction]) -> None:
        """
        Проверяет учет регистра при подсчете категорий.
        """
        categories = ["ПЕРЕВОД организации", "Перевод организации"]
        result = count_categories(test_transactions, categories)

        assert result["ПЕРЕВОД организации"] == 1
        assert result["Перевод организации"] == 1

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
        assert count_categories([], []) == {}

    def test_none_description(self, test_transactions: List[Transaction]) -> None:
        """
        Проверяет обработку транзакций с пустым описанием (None).
        """
        categories = ["None"]
        result = count_categories(test_transactions, categories)
        assert result["None"] == 0

    def test_duplicate_categories(self, test_transactions: List[Transaction]) -> None:
        """
        Проверяет обработку дублирующихся категорий в списке.
        """
        categories = ["Перевод организации", "Перевод организации"]
        result = count_categories(test_transactions, categories)
        assert len(result) == 2
        assert list(result.values()).count(1) == 2