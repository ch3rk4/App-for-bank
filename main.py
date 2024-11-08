#from src.masks import get_mask_account, get_mask_card_number
from src.widget import mask_account_card

card_date = str(input("Введите данные: "))

print(mask_account_card(card_date))