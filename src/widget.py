from src.masks import get_mask_account, get_mask_card_number

def mask_account_card(user_date: str) -> str:
    last_space = user_date.rfind(" ")

    if last_space == -1:
        return "Ошибка в вводе данных"

    number = user_date[last_space + 1:]

    if "Счет" or "Счёт" in user_date:
        if len(number) == 20:
            n_date = get_mask_account(number)
            return f"{user_date[:last_space]} {n_date}"
        else:
            return "Ошшибка в вводе данных"
    else:
        if len(number) == 16:
            n_date = get_mask_card_number(number)
            return f"{user_date[:last_space]} {n_date}"
        else:
            return "Ошшибка в вводе данных"
