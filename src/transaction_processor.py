import re
from collections import Counter
from typing import List

from src.finance_reader.types import Transaction


def search_transactions(transactions: List[Transaction], search_string: str) -> List[Transaction]:
    """
    Поиск транзакций по описанию с помощью регулярного выражения.
    """
    if not search_string:
        return transactions

    try:
        # Создаем регулярное выражение с игнорированием регистра
        pattern = re.compile(search_string, re.IGNORECASE)

        # Фильтруем транзакции, ищем совпадения в описании
        filtered_transactions = [
            transaction for transaction in transactions
            if pattern.search(transaction["description"])
        ]

        return filtered_transactions

    except re.error:
        # В случае некорректного регулярного выражения возвращаем пустой список
        return []


def count_categories(transactions: List[Transaction], categories: List[str]) -> dict[str, int]:
    """
    Подсчёт транзакций по категориям.
    """
    if not transactions or not categories:
        return {cat: 0 for cat in categories} if categories else {}

    counts = Counter(
        transaction["description"] for transaction in transactions if transaction["description"] in categories
    )

    return {cat: counts.get(cat, 0) for cat in categories}
