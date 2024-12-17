import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data/latest"


def convert_to_rubles(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли, используя Exchange Rates Data API.
    """
    if API_KEY is None:
        raise ValueError("API key not found in environment variables")

    amount = float(transaction["operationAmount"]["amount"])
    currency = transaction["operationAmount"]["currency"]["code"]

    if currency == "RUB":
        return amount

    if currency not in ("USD", "EUR"):
        raise ValueError(f"Unsupported currency: {currency}")

    try:
        response = requests.get(
            BASE_URL, headers={"apikey": API_KEY}, params={"base": currency, "symbols": "RUB"}, timeout=10
        )
        response.raise_for_status()

        data = response.json()

        try:
            rate = data["rates"]["RUB"]
            return amount * rate #type: ignore
        except KeyError:
            raise ValueError("Failed to get RUB rate from API response")

    except requests.RequestException as e:
        raise ValueError(f"Failed to get exchange rate: {str(e)}")
