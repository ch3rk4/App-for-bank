import pytest

from src.widget import get_date, mask_account_card
from tests.conftest import error_


def test_mask_account_card_1(card_1):
    """Тест корректного ввода"""
    assert mask_account_card("Visa Platinum 7000792289606361") == card_1


def test_mask_account_card_2(card_2):
    """Тест корректного ввода"""
    assert mask_account_card("Maestro 7000792289606361") == card_2


def test_mask_account_card_3(account_1):
    """Тест корректного ввода"""
    assert mask_account_card("Счет 73654108430135874305") == account_1


def test_mask_account_card_4(error_):
    """Тест номера с буквами"""
    assert mask_account_card("Visa Platinum 7000792ab9606361") == error_


def test_mask_account_card_5(error_):
    """Тест номера с меньшим количеством цифр"""
    assert mask_account_card("Visa Platinum 70007929606361") == error_


def test_mask_account_card_6(error_):
    """Тест номера без названия карты/счёта"""
    assert mask_account_card("70007929606361") == error_


def test_mask_account_card_7():
    """Тест на корректность работы буквы 'ё'"""
    assert mask_account_card("Счёт 73654108430135874305") == "Счёт **4305"


def test_mask_account_card_8(error_):
    """Тест на буквы в номере счёта"""
    assert mask_account_card("Счёт 736541084abc35874305") == error_


def test_mask_account_card_9(error_):
    """Тест на некорректное количество цифр в номере счёта"""
    assert mask_account_card("Счёт 73654108435874305") == error_


def test_mask_account_card_11(error_):
    """Тест на наличие пробелов в номере карты"""
    assert mask_account_card("Maestro 7000792 89606361") == error_


def test_mask_account_card_12(error_):
    """Тест на пустую строку"""
    assert mask_account_card("") == error_


@pytest.mark.parametrize(
    "value, expected",
    [
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Счет 35383033474447895560", "Счет **5560"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
        ("Visa Platinum 8990922113665229", "Visa Platinum 8990 92** **** 5229"),
        ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ],
)
def test_mask_account_card(value, expected):
    assert mask_account_card(value) == expected


def test_valid_date_format(date_):
    """Тест корректного формата даты"""
    assert get_date("2024-03-11T02:26:18.671407") == date_


def test_invalid_length(error_):
    """Тест неправильной длины входной строки"""
    assert get_date("2024-03-11") == error_


def test_space_in_date(error_):
    """Тест наличия пробела в дате"""
    assert get_date("2024-03-11 02:26:18.671407") == error_


def test_invalid_date_format(error_):
    """Тест неправильного формата даты"""
    assert get_date("11-03-202402:26:18.671407") == error_


def test_invalid_month(error_):
    """Тест неправильного месяца"""
    assert get_date("2024-13-1102:26:18.671407") == error_


def test_invalid_day(error_):
    """Тест неправильного дня"""
    assert get_date("2024-03-3202:26:18.671407") == error_


def test_invalid_input_type(error_):
    """Тест неправильного типа входных данных"""
    assert get_date(123) == error_


def test_empty_string(error_):
    """Тест пустой строки"""
    assert get_date("") == error_


def test_wrong_separator(error_):
    """Тест неправильного разделителя в дате"""
    assert get_date("2024/03/1102:26:18.671407") == error_


def test_missing_time(error_):
    """Тест отсутствия времени"""
    assert get_date("2024-03-11") == error_


def test_leap_year_valid():
    """Тест корректной даты високосного года"""
    assert get_date("2024-02-29T02:26:18.671407") == "29.02.2024"


def test_leap_year_invalid(error_):
    """Тест некорректной даты високосного года"""
    assert get_date("2023-02-2902:26:18.671407") == error_
