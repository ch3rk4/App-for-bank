def filter_by_state(operations: list[dict] = None, state: str = "EXECUTED") -> list[dict]:
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


def sort_by_date(operations: list[dict], reverse: bool = True) -> list[dict]:
    """
    Сортирует список операций по дате
    Sorts list ops by date
    """
    return sorted(operations, key=lambda x: x["date"], reverse=reverse)
