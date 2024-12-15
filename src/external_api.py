import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
BASE_URL = "http://api.exchangeratesapi.io/v1/latest"


def convert_to_rubles(transaction: Dict[str, Any]) -> float:
    amount = float(transaction["operationAmount"]["amount"])
    currency = transaction["operationAmount"]["currency"]["code"]

    if currency == "RUB":
        return amount

    try:
        response = requests.get(f"{BASE_URL}", params={"access_key": API_KEY, "base": currency, "symbols": "RUB"})
        data = response.json()
        rate = data["rates"]["RUB"]
        return amount * rate #type: ignore
    except Exception as e:
        raise ValueError(f"Failed to convert currency: {str(e)}")
