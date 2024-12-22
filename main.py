"""
 src.processing import filter_by_state, sort_by_date
from src.widget import get_date, mask_account_card

card_date = str(input("Введите данные: "))
date = str(input("Введите дату: "))

print(mask_account_card(card_date))
print(get_date(date))

test_operations = [
    {"id": 41428829, "state": "EXECUTED", "date": "2017-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]

filter_ = filter_by_state(test_operations)

print(sort_by_date(filter_))  # type: ignore
"""

from src.masks import get_mask_account, get_mask_card_number
from src.utils import load_operations


def process_operations() -> None:
    """
    Основная функция для обработки и вывода операций
    """
    operations = load_operations("data/operations.json")

    if not operations:
        print("Операции не найдены")
        return

    successful_operations = [op for op in operations if op.get("state") == "EXECUTED"]
    recent_operations = sorted(successful_operations, key=lambda x: x.get("date", ""), reverse=True)[:5]

    for operation in recent_operations:
        date_str = operation.get("date", "").split("T")[0]
        date_parts = date_str.split("-")
        if len(date_parts) == 3:
            formatted_date = f"{date_parts[2]}.{date_parts[1]}.{date_parts[0]}"
        else:
            formatted_date = "Дата не указана"

        description = operation.get("description", "Операция")

        from_account = operation.get("from_", "")
        if from_account:
            parts = from_account.split()
            if "Счет" in from_account:
                masked_from = f"{' '.join(parts[:-1])} {get_mask_account(parts[-1])}"
            else:
                masked_from = f"{' '.join(parts[:-1])} {get_mask_card_number(parts[-1])}"
        else:
            masked_from = "Отправитель не указан"

        to_account = operation.get("to", "")
        if to_account:
            parts = to_account.split()
            if "Счет" in to_account:
                masked_to = f"{' '.join(parts[:-1])} {get_mask_account(parts[-1])}"
            else:
                masked_to = f"{' '.join(parts[:-1])} {get_mask_card_number(parts[-1])}"
        else:
            masked_to = "Получатель не указан"

        operation_amount = operation.get("operationAmount", {})
        amount = operation_amount.get("amount", "0")
        currency = operation_amount.get("currency", {}).get("name", "")

        print(f"{formatted_date} {description}")
        print(f"{masked_from} -> {masked_to}")
        print(f"{amount} {currency}")
        print()


if __name__ == "__main__":
    process_operations()
