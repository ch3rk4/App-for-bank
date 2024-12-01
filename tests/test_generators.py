from typing import List, Iterator, Generator, Match, Optional
import pytest
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator
from tests.conftest import Transaction
import re
from typing_extensions import TypeGuard

CardNumber = str


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


def test_returns_usd_transaction_descriptions(transaction: List[Transaction]) -> None:
    """
    Проверяет корректность возврата описаний USD транзакций.
    """
    expected_descriptions: List[str] = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод с карты на карту"
    ]
    result: List[str] = list(transaction_descriptions(transaction, "USD"))
    assert result == expected_descriptions


def test_returns_rub_transaction_descriptions(transaction: List[Transaction]) -> None:
    """
    Проверяет корректность возврата описаний RUB транзакций.
    """
    expected_descriptions: List[str] = [
        "Перевод со счета на счет",
        "Перевод организации"
    ]
    result: List[str] = list(transaction_descriptions(transaction, "RUB"))
    assert result == expected_descriptions


def test_handles_empty_transaction_list() -> None:
    """
    Проверяет обработку пустого списка транзакций.
    Функция должна вернуть пустой итератор.
    """
    empty_transactions: List[Transaction] = []
    result: List[str] = list(transaction_descriptions(empty_transactions, "USD"))
    assert result == []


def test_handles_invalid_currency(transaction: List[Transaction]) -> None:
    """
    Проверяет обработку несуществующей валюты.
    """
    result: List[str] = list(transaction_descriptions(transaction, "EUR"))
    assert result == []


def test_returns_iterator_type(transaction: List[Transaction]) -> None:
    """
    Проверяет, что функция возвращает итератор, а не список.
    """
    result: Iterator[str] = transaction_descriptions(transaction, "USD")
    assert hasattr(result, '__iter__')
    assert not isinstance(result, list)


@pytest.mark.parametrize("currency_code,expected_count", [
    ("USD", 3),
    ("RUB", 2),
    ("EUR", 0)
])
def test_transaction_counts_by_currency(
        transaction: List[Transaction],
        currency_code: str,
        expected_count: int
) -> None:
    """
    Параметризованный тест для проверки количества транзакций разных валют.
    """
    result: List[str] = list(transaction_descriptions(transaction, currency_code))
    assert len(result) == expected_count


def test_single_transaction() -> None:
    """
    Проверяет работу функции с одной корректно структурированной транзакцией.
    """
    single_transaction: Transaction = {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Тестовый перевод",
        "from_": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702"
    }

    result: List[str] = list(transaction_descriptions([single_transaction], "USD"))
    assert result == ["Тестовый перевод"]


def is_valid_card_format(card_number: str) -> TypeGuard[CardNumber]:
    """
    Проверяет, соответствует ли строка формату номера карты.
    Используется как охранное выражение типа (type guard).
    """
    pattern = r'^\d{4} \d{4} \d{4} \d{4}$'
    return bool(re.match(pattern, card_number))



class TestCardNumberGenerator:
    def test_card_number_format(self) -> None:
        """Проверяет правильность форматирования номеров карт."""
        generator: Generator[CardNumber, None, None] = card_number_generator(
            "0000 0000 0000 0001",
            "0000 0000 0000 0010"
        )
        pattern: str = r'^\d{4} \d{4} \d{4} \d{4}$'

        for card_number in generator:
            match: Optional[Match[str]] = re.match(pattern, card_number)
            assert match is not None, f"Неверный формат номера карты: {card_number}"
            assert len(card_number) == 19, f"Неверная длина номера карты: {card_number}"

    def test_sequential_generation(self) -> None:
        """Проверяет последовательную генерацию номеров."""
        start: CardNumber = "0000 0000 0000 0001"
        end: CardNumber = "0000 0000 0000 0005"
        generator = card_number_generator(start, end)

        expected: list[CardNumber] = [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003",
            "0000 0000 0000 0004",
            "0000 0000 0000 0005"
        ]

        generated: list[CardNumber] = list(generator)
        assert generated == expected, "Последовательность номеров не соответствует ожидаемой"

    def test_range_boundaries(self) -> None:
        """Проверяет корректность обработки граничных значений диапазона."""
        # Проверка минимального значения
        min_generator = card_number_generator("0000 0000 0000 0001", "0000 0000 0000 0002")
        first_number: CardNumber = next(min_generator)
        assert first_number == "0000 0000 0000 0001"

        # Проверка максимального значения
        max_generator = card_number_generator("9999 9999 9999 9998", "9999 9999 9999 9999")
        numbers: list[CardNumber] = list(max_generator)
        assert numbers[-1] == "9999 9999 9999 9999"

    def test_empty_range(self) -> None:
        """Проверяет обработку пустого диапазона."""
        generator = card_number_generator("0000 0000 0000 0002", "0000 0000 0000 0001")
        with pytest.raises(StopIteration):
            next(generator)

    def test_invalid_input_format(self) -> None:
        """Проверяет обработку неверного формата входных данных."""
        invalid_formats: list[tuple[str, str]] = [
            ("000 0000 0000 0001", "0000 0000 0000 0002"),  # Неверное количество цифр
            ("0000-0000-0000-0001", "0000 0000 0000 0002"),  # Неверный разделитель
            ("abcd efgh ijkl mnop", "0000 0000 0000 0002"),  # Нецифровые символы
        ]

        for start, end in invalid_formats:
            with pytest.raises(ValueError):
                next(card_number_generator(start, end))