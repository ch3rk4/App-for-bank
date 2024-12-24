from typing import List, Dict
import re
from collections import Counter


def search_transactions(transactions: List[Dict], search_string: str) -> List[Dict]:
    """
    Поиск транзакций по описанию с помощью регулярного выражения.
    """
    if not search_string:
        return transactions

    pattern = re.compile(search_string, re.IGNORECASE)
    return [
        transaction for transaction in transactions
        if pattern.search(transaction.get("description", ""))
    ]


def count_categories(transactions: List[Dict], categories: List[str]) -> Dict[str, int]:
    """
    Подсчёт транзакций по категориям.
    """
    if not transactions or not categories:
        return {cat: 0 for cat in categories} if categories else {}

    counts = Counter(
        transaction.get("description") for transaction in transactions
        if transaction.get("description") in categories
    )

    return {cat: counts.get(cat, 0) for cat in categories}