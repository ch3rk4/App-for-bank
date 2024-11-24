from src.processing import filter_by_state


def test_filter_executed(sample_operations):
    """Тест фильтрации EXECUTED операций"""
    result = filter_by_state(sample_operations, "EXECUTED")
    assert len(result) == 2
    assert all(op['state'] == 'EXECUTED' for op in result)
    assert result[0]['id'] == 41428829
    assert result[1]['id'] == 939719570

def test_filter_canceled(sample_operations):
    """Тест фильтрации CANCELED операций"""
    result = filter_by_state(sample_operations, "CANCELED")
    assert len(result) == 2
    assert all(op['state'] == 'CANCELED' for op in result)
    assert result[0]['id'] == 594226727
    assert result[1]['id'] == 615064591

def test_default_state(sample_operations):
    """Тест значения state по умолчанию (EXECUTED)"""
    result = filter_by_state(sample_operations)
    assert len(result) == 2
    assert all(op['state'] == 'EXECUTED' for op in result)

def test_empty_list(error_):
    """Тест пустого списка операций"""
    assert filter_by_state([]) == error_

def test_none_input(error_):
    """Тест None в качестве входных данных"""
    assert filter_by_state(None) == error_

def test_invalid_state(sample_operations, error_):
    """Тест несуществующего состояния"""
    result = filter_by_state(sample_operations, "INVALID_STATE")
    assert result == error_

def test_missing_state_key():
    """Тест отсутствующего ключа state"""
    operations = [
        {'id': 41428829, 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
    ]
    result = filter_by_state(operations)
    assert len(result) == 1
    assert result[0]['id'] == 939719570

def test_invalid_operation_type():
    """Тест некорректного типа операции"""
    operations = [
        None,
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        "not a dict",
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}
    ]
    result = filter_by_state(operations)
    assert len(result) == 2
    assert all(op['state'] == 'EXECUTED' for op in result)

def test_case_sensitive_state(sample_operations, error_):
    """Тест чувствительности к регистру"""
    result = filter_by_state(sample_operations, "executed")
    assert result == error_

def test_mixed_states():
    """Тест смешанных состояний, включая None и пустые строки"""
    operations = [
        {'id': 1, 'state': 'EXECUTED'},
        {'id': 2, 'state': None},
        {'id': 3, 'state': ''},
        {'id': 4, 'state': 'EXECUTED'}
    ]
    result = filter_by_state(operations)
    assert len(result) == 2
    assert all(op['state'] == 'EXECUTED' for op in result)