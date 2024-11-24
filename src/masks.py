def get_mask_card_number(card_number: str or int) -> str:
    """Func that masks card's number"""
    s_card_number = str(card_number)

    if " " in s_card_number:
        str_card_number = s_card_number.replace(" ", "")
    else:
        str_card_number = s_card_number

    if len(str_card_number) != 16 or not str_card_number.isdigit():
        return "Ошибка ввода"
    else:
        numbers = []

        for number in str_card_number:

            numbers.append(number)

        start_index = 6

        end_index = -4

        numbers[start_index:end_index] = ["*"] * (len(numbers) + end_index - start_index)

        mask_card = "".join(numbers)

        mask_card_number = " ".join(mask_card[i : i + 4] for i in range(0, len(mask_card), 4))

        return mask_card_number


def get_mask_account(account_number: str or int) -> str:
    """Func that masks account's number"""
    str_account_number = str(account_number)

    if len(str_account_number) != 20:
        return "Ошибка ввода"
    else:
        ac_numbers = []

        length = len(str_account_number)

        for i, ac_number in enumerate(str_account_number):

            if length - 4 > i:

                ac_numbers.append("*")

            else:

                ac_numbers.append(ac_number)

        mask_ac_numbers = ac_numbers[-6:]

        return "".join(mask_ac_numbers)
