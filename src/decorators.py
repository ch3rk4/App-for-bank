import functools
import sys
from typing import Any, Callable, Optional, TypeVar

R = TypeVar('R')


def log(filename: Optional[str] = None) -> Callable[[Callable[..., R]], Callable[..., R]]:
    """
    Декоратор для логирования выполнения функции.
    """

    def decorator(func: Callable[..., R]) -> Callable[..., R]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> R:
            try:
                result = func(*args, **kwargs)
                log_message = f"{func.__name__} ok\n"
            except Exception as e:
                args_str = str(args)[1:-1] if len(args) != 1 else str(args)[1:-2]

                log_message = (
                    f"{func.__name__} error: {str(e)}. "
                    f"Inputs: ({args_str}), {kwargs}\n"
                )
                raise
            finally:
                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(log_message)
                else:
                    sys.stdout.write(log_message)
                    sys.stdout.flush()

            return result

        return wrapper

    return decorator