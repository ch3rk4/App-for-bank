from datetime import datetime, timezone
from unittest.mock import mock_open, patch
import pandas as pd
import pytest
from src.finance_reader.readers import read_transactions_csv, read_transactions_excel
from src.finance_reader.types import Transaction


@pytest.fixture
def sample_csv_content():
    return '''id;state;date;amount;currency_name;currency_code;from;to;description
650703;EXECUTED;2023-09-05T11:30:32Z;16210;Sol;PEN;Счет 58803664561298323391;Счет 39745660563456619397;Перевод организации'''


@pytest.fixture
def expected_transaction() -> Transaction:
    """
    Фикстура, возвращающая ожидаемую транзакцию с правильной датой в UTC.
    """
    return {
        'id': '650703',
        'state': 'EXECUTED',
        'date': datetime(2023, 9, 5, 11, 30, 32, tzinfo=timezone.utc),  # Добавили UTC
        'amount': 16210.0,
        'currency_name': 'Sol',
        'currency_code': 'PEN',
        'from_account': 'Счет 58803664561298323391',
        'to_account': 'Счет 39745660563456619397',
        'description': 'Перевод организации'
    }


def test_read_transactions_csv(sample_csv_content, expected_transaction):
    """Тест успешного чтения CSV файла."""
    with patch('builtins.open', mock_open(read_data=sample_csv_content)):
        transactions = read_transactions_csv('fake_path.csv')
        assert len(transactions) == 1
        assert transactions[0] == expected_transaction


def test_read_transactions_csv_file_not_found():
    """Тест обработки отсутствующего файла."""
    with pytest.raises(FileNotFoundError):
        read_transactions_csv('nonexistent.csv')


@pytest.fixture
def sample_excel_content():
    """Фикстура для создания тестового Excel-файла."""
    import io
    import pandas as pd

    df = pd.DataFrame([{
        'id': '650703',
        'state': 'EXECUTED',
        'date': '2023-09-05T11:30:32Z',
        'amount': 16210,
        'currency_name': 'Sol',
        'currency_code': 'PEN',
        'from': 'Счет 58803664561298323391',
        'to': 'Счет 39745660563456619397',
        'description': 'Перевод организации'
    }])

    buffer = io.BytesIO()
    df.to_excel(buffer, index=False)
    return buffer.getvalue()


def test_read_transactions_excel(sample_excel_content, expected_transaction):
    """Тест успешного чтения Excel файла."""
    with patch('builtins.open', mock_open(read_data=sample_excel_content)):
        with patch('pandas.read_excel') as mock_read_excel:
            mock_read_excel.return_value = pd.DataFrame([{
                'id': '650703',
                'state': 'EXECUTED',
                'date': '2023-09-05T11:30:32Z',
                'amount': 16210,
                'currency_name': 'Sol',
                'currency_code': 'PEN',
                'from': 'Счет 58803664561298323391',
                'to': 'Счет 39745660563456619397',
                'description': 'Перевод организации'
            }])
            transactions = read_transactions_excel('fake_path.xlsx')
            assert len(transactions) == 1
            assert transactions[0] == expected_transaction