from src.widget import mask_account_card


def test_mask_account_card_1(card_1):
    assert mask_account_card("Visa Platinum 7000792289606361") == card_1


def test_mask_account_card_2(card_2):
    assert mask_account_card("Maestro 7000792289606361") == card_2


def test_mask_account_card_3(account_1):
    assert mask_account_card("Счет 73654108430135874305") == account_1