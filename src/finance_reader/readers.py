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
                # Пропускаем транзакции со статусом PENDING
                if row["state"] not in ["EXECUTED", "CANCELED"]:
                    continue

                # Преобразуем дату из строки в datetime
                date_str = row["date"].strip()
                if not date_str:
                    continue  # Пропускаем строки с пустой датой

                try:
                    date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                except ValueError:
                    continue  # Пропускаем строки с некорректной датой

                # Преобразуем сумму в float
                try:
                    amount = float(row["amount"])
                except ValueError:
                    continue  # Пропускаем строки с некорректной суммой

                transaction: Transaction = {
                    "id": row["id"],
                    "state": row["state"],  # type: ignore
                    "date": date,
                    "amount": amount,
                    "currency_name": row["currency_name"],
                    "currency_code": row["currency_code"],
                    "from_account": row["from"],  # Переименовываем поле
                    "to_account": row["to"],  # Переименовываем поле
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
        # Читаем все столбцы как строки, чтобы избежать автоматического преобразования типов
        df = pd.read_excel(
            file_path,
            dtype={
                "id": str,
                "state": str,
                "date": str,
                "amount": float,
                "currency_name": str,
                "currency_code": str,
                "from": str,
                "to": str,
                "description": str,
            },
        )

        transactions: List[Transaction] = []

        for _, row in df.iterrows():
            # Пропускаем строки с неподдерживаемым статусом
            if row["state"] not in ["EXECUTED", "CANCELED"]:
                continue

            # Обрабатываем дату, учитывая возможные форматы из Excel
            try:
                # Если дата пришла как строка в ISO формате
                if isinstance(row["date"], str):
                    date = datetime.fromisoformat(row["date"].replace("Z", "+00:00"))
                # Если дата пришла как timestamp из Excel
                else:
                    date = pd.to_datetime(row["date"]).to_pydatetime()
            except (ValueError, AttributeError):
                continue  # Пропускаем строки с некорректной датой

            # Пропускаем строки с отсутствующими обязательными данными
            if pd.isna(row["id"]) or pd.isna(row["amount"]):
                continue

            transaction: Transaction = {
                "id": str(row["id"]),  # Преобразуем в строку, так как id должен быть строкой
                "state": row["state"],  # type: ignore
                "date": date,
                "amount": float(row["amount"]),
                "currency_name": str(row["currency_name"]),
                "currency_code": str(row["currency_code"]),
                "from_account": str(row["from"]),
                "to_account": str(row["to"]),
                "description": str(row["description"]),
            }
            transactions.append(transaction)

        return transactions

    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {file_path} не найден")
    except Exception as e:
        raise ValueError(f"Ошибка формата данных: {str(e)}")
