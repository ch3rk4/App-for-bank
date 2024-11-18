def filter_by_state(operations: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Фильтрует список словарей по значению ключа state
    Filters list of dicts val by state key
    """
    filtered_operations = []
    for operation in operations:
        operation_state = operation.get("state")

        if operation_state == state:
            filtered_operations.append(operation)

    return filtered_operations


def sort_by_date(operations: list[dict], reverse: bool = True) -> list[dict]:
    """
    Сортирует список операций по дате
    Sorts list ops by date
    """
    return sorted(operations, key=lambda x: x["date"], reverse=reverse)
