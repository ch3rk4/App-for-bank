import pytest
from typing import Any
from pathlib import Path
from decorators import log


def test_successful_console_output(capsys: pytest.CaptureFixture) -> None:
    """
    Тестирование успешного вывода в консоль.
    """
    @log()
    def add(x: int, y: int) -> int:
        return x + y

    result = add(1, 2)
    captured = capsys.readouterr()

    assert result == 3
    assert "add ok" in captured.out


def test_successful_file_output(tmp_path: Path) -> None:
    """
    Тестирование успешного вывода в файл.
    """
    log_file = tmp_path / "test_log.txt"

    @log(filename=str(log_file))
    def multiply(x: int, y: int) -> int:
        return x * y

    result = multiply(2, 3)

    assert result == 6
    assert log_file.exists()

    with open(log_file, 'r') as f:
        content = f.read()
        assert "multiply ok" in content


def test_error_console_output(capsys: pytest.CaptureFixture) -> None:
    """
    Тестирование вывода ошибок в консоль.
    """

    @log()
    def divide(x: int, y: int) -> float:
        return x / y

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    captured = capsys.readouterr()
    assert "divide error: division by zero" in captured.out
    assert "Inputs: (1, 0), {}" in captured.out


def test_error_file_output(tmp_path: Path) -> None:
    """
    Тестирование записи ошибок в файл.
    """
    log_file = tmp_path / "error_log.txt"

    @log(filename=str(log_file))
    def access_invalid_index(lst: list) -> Any:
        return lst[10]

    with pytest.raises(IndexError):
        access_invalid_index([1, 2, 3])

    assert log_file.exists()
    with open(log_file, 'r') as f:
        content = f.read()
        assert "access_invalid_index error: list index out of range" in content
        assert "Inputs: ([1, 2, 3]), {}" in content


def test_decorator_preserves_function_metadata() -> None:
    """
    Тестирование сохранения метаданных декорируемой функции.
    """

    @log()
    def example_function(x: int) -> int:
        """Example docstring."""
        return x * 2

    assert example_function.__name__ == "example_function"
    assert example_function.__doc__ == "Example docstring."


def test_multiple_calls_same_file(tmp_path: Path) -> None:
    """
    Тестирование множественных вызовов с записью в один файл.
    """
    log_file = tmp_path / "multiple_log.txt"

    @log(filename=str(log_file))
    def simple_func(x: int) -> int:
        return x + 1

    simple_func(1)
    simple_func(2)

    with open(log_file, 'r') as f:
        content = f.read()
        assert content.count("simple_func ok") == 2


def test_kwargs_logging(capsys: pytest.CaptureFixture) -> None:
    """
    Тестирование логирования именованных аргументов.
    """

    @log()
    def greet(name: str, greeting: str = "Hello") -> str:
        return f"{greeting}, {name}!"

    greet("World", greeting="Hi")
    captured = capsys.readouterr()
    assert "greet ok" in captured.out