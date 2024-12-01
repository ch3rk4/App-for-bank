from typing import Iterator, List
from tests.conftest import Transaction

def filter_by_currency(transactions: List[Transaction], cur: str) -> Iterator[Transaction]:
    """

    """
    if not cur.isupper():
        return iter([]) # type: ignore
    for transaction in transactions:
        try:
            if transaction["operationAmount"]["currency"]["code"] == cur:
                yield transaction
        except KeyError:
            continue


def transaction_descriptions(transactions: List[Transaction], cur: str) -> Iterator[str]:
    """

    """
    if not cur.isupper():
        return iter([]) # type: ignore
    for transaction in transactions:
        try:
            if transaction["operationAmount"]["currency"]["code"] == cur:
                yield transaction["description"]
        except KeyError:
            continue


#def card_number_generator():