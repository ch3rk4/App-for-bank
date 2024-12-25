import json
from unittest import TestCase, mock

from src.utils import load_operations


class TestUtils(TestCase):
    def setUp(self) -> None:
        """
        Тест загрузки операций из Json-файла
        """
        self.test_data = [
            {
                "id": 939719570,
                "state": "EXECUTED",
                "date": "2018-06-30T02:08:58.425572",
                "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
                "description": "Перевод организации",
                "from_": "Счет 75106830613657916952",
                "to": "Счет 11776614605963066702",
            }
        ]

    def test_load_operations_success(self) -> None:
        """
        Тест успешного сценария
        """
        with mock.patch("builtins.open", mock.mock_open(read_data=json.dumps(self.test_data))):
            result = load_operations("dummy_path.json")
            self.assertEqual(result, self.test_data)

    def test_load_operations_empty_file(self) -> None:
        """
        Тест пустого файла
        """
        with mock.patch("builtins.open", mock.mock_open(read_data="")):
            result = load_operations("dummy_path.json")
            self.assertEqual(result, [])

    def test_load_operations_invalid_json(self) -> None:
        """
        Тест некорректного JSON-файла
        """
        with mock.patch("builtins.open", mock.mock_open(read_data="invalid json")):
            result = load_operations("dummy_path.json")
            self.assertEqual(result, [])

    def test_load_operations_not_list(self) -> None:
        """
        Тест файла с пустым списком
        """
        with mock.patch("builtins.open", mock.mock_open(read_data='{"key": "value"}')):
            result = load_operations("dummy_path.json")
            self.assertEqual(result, [])

    def test_load_operations_file_not_found(self) -> None:
        """
        Тест случая, когда файла нет
        """
        result = load_operations("nonexistent.json")
        self.assertEqual(result, [])
