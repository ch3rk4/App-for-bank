import logging
from typing import Union

# Создаем и настраиваем логер
logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)

# Создаем обработчик для записи в файл
file_handler = logging.FileHandler("logs/masks.log", mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Создаем форматтер для логов
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)

# Добавляем обработчик к логеру
logger.addHandler(file_handler)


def get_mask_card_number(card_number: Union[str, int]) -> str:
    """
    Функция маскирует номер карты, оставляя видимыми первые 6 и последние 4 цифры
    """
    s_card_number = str(card_number)
    logger.debug(f"Получен номер карты для маскировки: {card_number}")

    if " " in s_card_number:
        str_card_number = s_card_number.replace(" ", "")
        logger.debug("Удалены пробелы из номера карты")
    else:
        str_card_number = s_card_number

    if len(str_card_number) != 16 or not str_card_number.isdigit():
        logger.error(
            f"Некорректный номер карты: {card_number}. "
            f"Длина: {len(str_card_number)}, является числом: {str_card_number.isdigit()}"
        )
        return "Ошибка ввода"

    numbers = list(str_card_number)
    start_index = 6
    end_index = -4
    numbers[start_index:end_index] = ["*"] * (len(numbers) + end_index - start_index)

    mask_card = "".join(numbers)
    mask_card_number = " ".join(mask_card[i : i + 4] for i in range(0, len(mask_card), 4))

    logger.info(f"Успешно замаскирован номер карты. Результат: {mask_card_number}")
    return mask_card_number


def get_mask_account(account_number: Union[str, int]) -> str:
    """
    Функция маскирует номер счета, оставляя видимыми только последние 6 цифры
    """
    str_account_number = str(account_number)
    logger.debug(f"Получен номер счета для маскировки: {account_number}")

    if len(str_account_number) != 20 or not str_account_number.isdigit():
        logger.error(
            f"Некорректный номер счета: {account_number}. "
            f"Длина: {len(str_account_number)}, является числом: {str_account_number.isdigit()}"
        )
        return "Ошибка ввода"

    ac_numbers = ["*" if i < len(str_account_number) - 4 else num for i, num in enumerate(str_account_number)]
    mask_ac_numbers = ac_numbers[-6:]
    result = "".join(mask_ac_numbers)

    logger.info(f"Успешно замаскирован номер счета. Результат: {result}")
    return result
