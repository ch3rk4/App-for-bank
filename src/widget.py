from src.masks import get_mask_account, get_mask_card_number

def mask_account_card(card_date: str) -> str:
    last_space = card_date.rfind(" ")

    if last_space == -1:
        return "Ошибка в вводе данных"

    number = card_date[last_space + 1:]

    if "Счёт" in card_date:
        if len(number) == 20:
            n_date = get_mask_account(number)
            return f"{card_date[:last_space]} {n_date}"
        else:
            return "Ошшибка в вводе данных"
    else:
        if len(number) == 16:
            n_date = get_mask_card_number(number)
            return f"{card_date[:last_space]} {n_date}"
        else:
            return "Ошшибка в вводе данных"
