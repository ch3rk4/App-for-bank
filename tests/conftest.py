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