from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(user_date: str) -> str:
    "Func that masks user's date"
    last_space = user_date.rfind(" ")

    if last_space == -1:
        return "Ошибка ввода"

    number = user_date[last_space + 1 :]

    if "Счет" in user_date or "Счёт" in user_date:
        n_date = get_mask_account(number)
        if "Ошибка ввода" in n_date:
            return "Ошибка ввода"
        else:
            return f"{user_date[:last_space]} {n_date}"
    else:
        n_date = get_mask_card_number(number)
        if "Ошибка ввода" in n_date:
            return "Ошибка ввода"
        else:
            return f"{user_date[:last_space]} {n_date}"


def get_date(date: str) -> str:
    "Func that shows date like 'DD.MM.YYYY'"
    if not isinstance(date, str):
        return "Ошибка ввода"
    if len(date) != 26 or " " in date:
        return "Ошибка ввода"
    try:
        n_date = date[0:10].split("-")
        if not (len(n_date[0]) == 4 and len(n_date[1]) == 2 and len(n_date[2]) == 2):
            return "Ошибка ввода"
        datetime.strptime(date[0:10], "%Y-%m-%d")
        return ".".join(n_date[::-1])
    except (ValueError, IndexError):
        return "Ошибка ввода"
