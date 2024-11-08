from src.widget import get_date, mask_account_card

card_date = str(input("Введите данные: "))
date = str(input("Введите дату: "))

print(mask_account_card(card_date))
print(get_date(date))
