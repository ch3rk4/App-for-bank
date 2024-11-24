def get_mask_card_number(card_number: str or int) -> str:
    """Func that masks card's number"""
    str_card_number = str(card_number)
    numbers = []

    for number in str_card_number:

        numbers.append(number)

    start_index = 6

    end_index = -4

    numbers[start_index:end_index] = ["*"] * (len(numbers) + end_index - start_index)

    mask_card = "".join(numbers)

    str_mask_card_number = " ".join(mask_card[i : i + 4] for i in range(0, len(mask_card), 4))

    return str_mask_card_number


def get_mask_account(account_number: str) -> str:
    """Func that masks account's number"""
    ac_numbers = []

    length = len(account_number)

    for i, ac_number in enumerate(account_number):

        if length - 4 > i:

            ac_numbers.append("*")

        else:

            ac_numbers.append(ac_number)

    mask_ac_numbers = ac_numbers[-6:]

    return "".join(mask_ac_numbers)
