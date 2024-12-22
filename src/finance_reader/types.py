from typing import TypedDict, Literal
from datetime import datetime

class Transaction(TypedDict):
    """Структура финансовой операции."""
    id: str
    state: Literal['EXECUTED', 'CANCELED']
    date: datetime
    amount: float
    currency_name: str
    currency_code: str
    from_account: str
    to_account: str
    description: str