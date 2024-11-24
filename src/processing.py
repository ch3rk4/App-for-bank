from datetime import datetime


def filter_by_state(operations: list[dict], state: str = "EXECUTED") -> list[dict] | str:
    """
    Фильтрует список словарей по значению ключа state
    Filters list of dicts val by state key
    """
    if operations is None or not isinstance(operations, list):
        return "Ошибка ввода"

    filtered_operations = []
    for operation in operations:
        if not isinstance(operation, dict):
            continue

        operation_state = operation.get("state")
        if operation_state == state:
            filtered_operations.append(operation)
    if filtered_operations == ([]):
        return "Ошибка ввода"
    return filtered_operations


def sort_by_date(operations: list[dict], reverse: bool = True) -> list[dict] | str:
    """
    Сортирует список операций по дате
    Sorts list ops by date
    """
    if operations is None:
        return "Ошибка ввода"

    if not isinstance(operations, list):
        return "Ошибка ввода"

    if operations == []:
        return "Ошибка ввода"

    valid_operations = []

    for operation in operations:
        if not isinstance(operation, dict):
            continue

        date = operation.get("date")
        if not date:
            continue

        try:
            datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
            valid_operations.append(operation)
        except ValueError:
            continue

    return sorted(valid_operations, key=lambda x: x["date"], reverse=reverse)
