from typing import Iterator, List
from tests.conftest import Transaction

def filter_by_currency(transactions: List[Transaction], cur: str) -> Iterator[Transaction]:
    if not cur.isupper():
        return iter([])
    for transaction in transactions:
        try:
            if transaction["operationAmount"]["currency"]["code"] == cur:
                yield transaction
        except KeyError:
            continue



#def transaction_descriptions():



#def card_number_generator():