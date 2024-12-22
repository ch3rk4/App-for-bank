import csv
from datetime import datetime
from typing import List

import pandas as pd

from .types import Transaction


def read_transactions_csv(file_path: str) -> List[Transaction]:
    """
    Читает финансовые операции из CSV файла.
    """
    transactions: List[Transaction] = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")
            for row in reader:
                transaction: Transaction = {
                    "id": row["id"],
                    "state": row["state"],
                    "date": datetime.fromisoformat(row["date"].replace("Z", "+00:00")),
                    "amount": float(row["amount"]),
                    "currency_name": row["currency_name"],
                    "currency_code": row["currency_code"],
                    "from_account": row["from"],
                    "to_account": row["to"],
                    "description": row["description"],
                }
                transactions.append(transaction)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {file_path} не найден")
    except (ValueError, KeyError) as e:
        raise ValueError(f"Ошибка формата данных: {str(e)}")

    return transactions


def read_transactions_excel(file_path: str) -> List[Transaction]:
    """
    Читает финансовые операции из Excel файла.
    """
    try:
        df = pd.read_excel(file_path)
        transactions: List[Transaction] = []

        for _, row in df.iterrows():
            transaction: Transaction = {
                "id": str(row["id"]),
                "state": row["state"],
                "date": datetime.fromisoformat(row["date"].replace("Z", "+00:00")),
                "amount": float(row["amount"]),
                "currency_name": row["currency_name"],
                "currency_code": row["currency_code"],
                "from_account": row["from"],
                "to_account": row["to"],
                "description": row["description"],
            }
            transactions.append(transaction)

        return transactions
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {file_path} не найден")
    except (ValueError, KeyError) as e:
        raise ValueError(f"Ошибка формата данных: {str(e)}")
