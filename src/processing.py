def filter_by_state(operations: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Фильтрует список словарей по значению ключа state
    Filters the list of dicts the val of the state key
    """
    filtered_operations = []
    for operation in operations:
        operation_state = operation.get("state")

        if operation_state == state:
            filtered_operations.append(operation)

    return filtered_operations
