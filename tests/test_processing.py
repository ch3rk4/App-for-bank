from datetime import datetime
from typing import Any, Dict, List, Union

from src.processing import filter_by_state, sort_by_date


def test_filter_by_state_valid_input(valid_operations: List[Dict[str, Any]]) -> None:
    result = filter_by_state(valid_operations)
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(op["state"] == "EXECUTED" for op in result)


def test_filter_by_state_none_input(error_: str) -> None:
    result = filter_by_state(None)  # type: ignore
    assert result == error_


def test_filter_by_state_empty_list(error_: str) -> None:
    result = filter_by_state([])
    assert result == error_


def test_filter_by_state_invalid_input(invalid_operations: List[Union[Dict[str, Any], str]]) -> None:
    result = filter_by_state(invalid_operations)  # type: ignore
    assert isinstance(result, list)
    assert len(result) == 1


def test_sort_by_date_valid_input(valid_operations: List[Dict[str, Any]]) -> None:
    result = sort_by_date(valid_operations)
    assert isinstance(result, list)
    assert len(result) == 4
    dates = [datetime.strptime(op["date"], "%Y-%m-%dT%H:%M:%S.%f") for op in result]
    assert dates == sorted(dates, reverse=True)


def test_sort_by_date_none_input(error_: str) -> None:
    result = sort_by_date(None)  # type: ignore
    assert result == error_


def test_sort_by_date_empty_list(error_: str) -> None:
    result = sort_by_date([])
    assert result == error_


def test_sort_by_date_invalid_date_format(invalid_date_operations: List[Dict[str, Any]]) -> None:
    result = sort_by_date(invalid_date_operations)
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["date"] == "2018-06-30T02:08:58.425572"


def test_sort_by_date_no_date_field(no_date_operations: List[Dict[str, Any]]) -> None:
    result = sort_by_date(no_date_operations)
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["date"] == "2018-06-30T02:08:58.425572"
