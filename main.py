from src.masks import get_mask_account, get_mask_card_number

card_number = str(input("Введите номер карты: "))
account_number = str(input("Введите номер счёта в банке: "))


if len(card_number) == 16 and len(account_number) == 20:
    print(get_mask_card_number(card_number))
    print(get_mask_account(account_number))
else:
    print("Ошшибка в вводе данных")
