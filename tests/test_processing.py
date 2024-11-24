from src.processing import filter_by_state, sort_by_date


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


def test_sort_desc(sample_operations):
    """Тест сортировки по убыванию (по умолчанию)"""
    result = sort_by_date(sample_operations)
    assert isinstance(result, list)
    assert len(result) == 4
    assert result[0]['date'] > result[1]['date']
    assert result[0]['id'] == 41428829
    assert result[-1]['id'] == 939719570

def test_sort_asc(sample_operations):
    """Тест сортировки по возрастанию"""
    result = sort_by_date(sample_operations, reverse=False)
    assert isinstance(result, list)
    assert len(result) == 4
    assert result[0]['date'] < result[1]['date']
    assert result[0]['id'] == 939719570
    assert result[-1]['id'] == 41428829

def test_none_input(error_):
    """Тест None в качестве входных данных"""
    result = sort_by_date(None)
    assert isinstance(result, str)
    assert result == error_

def test_invalid_input_type(error_):
    """Тест неверного типа входных данных"""
    result = sort_by_date("not a list")
    assert isinstance(result, str)
    assert result == error_

def test_empty_list(error_):
    """Тест пустого списка"""
    result = sort_by_date([])
    assert isinstance(result, str)  # проверяем что вернулась строка с ошибкой
    assert result == error_

def test_missing_date():
    """Тест отсутствующей даты"""
    operations = [
        {'id': 1, 'state': 'EXECUTED'},
        {'id': 2, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 3, 'state': 'EXECUTED', 'date': '2019-08-03T18:35:29.512364'}
    ]
    result = sort_by_date(operations)
    assert isinstance(result, list)
    assert len(result) == 2
    assert all('date' in op for op in result)

def test_invalid_date_format():
    """Тест неверного формата даты"""
    operations = [
        {'id': 1, 'date': 'invalid date'},
        {'id': 2, 'date': '2019-07-03T18:35:29.512364'},
        {'id': 3, 'date': '2019/08/03'}
    ]
    result = sort_by_date(operations)
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]['id'] == 2

def test_invalid_operation_type():
    """Тест некорректного типа операции внутри списка"""
    operations = [
        None,
        {'id': 1, 'date': '2019-07-03T18:35:29.512364'},
        "not a dict",
        {'id': 2, 'date': '2019-08-03T18:35:29.512364'}
    ]
    result = sort_by_date(operations)
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(op, dict) for op in result)

def test_same_dates():
    """Тест операций с одинаковыми датами"""
    operations = [
        {'id': 1, 'date': '2019-07-03T18:35:29.512364'},
        {'id': 2, 'date': '2019-07-03T18:35:29.512364'}
    ]
    result = sort_by_date(operations)
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]['date'] == result[1]['date']

def test_preserve_data():
    """Тест сохранения всех данных операции после сортировки"""
    operations = [
        {'id': 1, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364', 'amount': 100},
        {'id': 2, 'state': 'CANCELED', 'date': '2019-08-03T18:35:29.512364', 'amount': 200}
    ]
    result = sort_by_date(operations)
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(len(op) == 4 for op in result)