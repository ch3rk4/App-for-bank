from unittest import TestCase, mock

import requests

from src.external_api import convert_to_rubles


class TestExternalAPI(TestCase):
    def setUp(self) -> None:
        """
        Пример транзакций
        """
        self.usd_transaction = {"operationAmount": {"amount": "100.00", "currency": {"name": "USD", "code": "USD"}}}

        self.rub_transaction = {"operationAmount": {"amount": "100.00", "currency": {"name": "руб.", "code": "RUB"}}}

    @mock.patch("src.external_api.requests.get")
    def test_convert_usd_to_rubles(self, mock_get: mock.MagicMock) -> None:
        """
        Тест перевода из USD в RUB
        """
        mock_get.return_value.json.return_value = {"rates": {"RUB": 75.0}}
        result = convert_to_rubles(self.usd_transaction)
        self.assertEqual(result, 7500.0)

    def test_already_in_rubles(self) -> None:
        """
        Тест ситуации, когда валюта уже в RUB, и перевод не нужен
        """
        result = convert_to_rubles(self.rub_transaction)
        self.assertEqual(result, 100.0)

    @mock.patch("src.external_api.requests.get")
    def test_api_error(self, mock_get: mock.MagicMock) -> None:
        """Тест обработки ошибок API"""
        # Теперь используем правильный тип исключения
        mock_get.side_effect = requests.RequestException("API Error")

        with self.assertRaises(ValueError):
            convert_to_rubles(self.usd_transaction)

    @mock.patch("src.external_api.requests.get")
    def test_invalid_response_format(self, mock_get: mock.MagicMock) -> None:
        """Тест обработки некорректного формата ответа"""
        mock_get.return_value.json.return_value = {"incorrect": "format"}
        mock_get.return_value.raise_for_status = mock.Mock()

        with self.assertRaises(ValueError):
            convert_to_rubles(self.usd_transaction)
