import pytest

from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number_1(numbers_1):
    assert get_mask_card_number("7000792289606361") == numbers_1


def test_get_mask_account_1(numbers_1):
    with pytest.raises(AssertionError):
        assert get_mask_account("7000792289606361") == numbers_1


def test_get_mask_card_number_2(numbers_2):
    with pytest.raises(AssertionError):
        assert get_mask_card_number("73654108430135874305") == numbers_2


def test_get_mask_account_2(numbers_2):
    assert get_mask_account("73654108430135874305") == numbers_2


def test_get_mask_card_number_3(numbers_1):
    assert get_mask_card_number(7000792289606361) == numbers_1


def test_get_mask_account_3(numbers_2):
    assert get_mask_account(73654108430135874305) == numbers_2


def test_get_mask_card_number_4():
    assert get_mask_card_number("73654108430135874305") == "Ошибка ввода"


def test_get_mask_account_4():
    assert get_mask_account("7000792289606361") == "Ошибка ввода"


def test_get_mask_card_number_5(numbers_1):
    assert get_mask_card_number("7000 7922 8960 6361") == numbers_1


def  test_get_mask_card_number_6():
    assert get_mask_card_number("7000abc289606361") == "Ошибка ввода"


def test_get_mask_account_6():
    assert get_mask_account("736541abc30135874305") == "Ошибка ввода"