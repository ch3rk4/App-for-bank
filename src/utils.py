import json
import logging
from typing import Any, Dict, List

# Создаем и настраиваем логер для модуля utils
logger = logging.getLogger('utils')
logger.setLevel(logging.DEBUG)

# Создаем обработчик для записи в файл
file_handler = logging.FileHandler('logs/utils.log', mode='w', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

# Создаем форматтер для логов с тем же форматом, что и в masks
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Добавляем обработчик к логеру
logger.addHandler(file_handler)


def load_operations(file_path: str) -> List[Dict[str, Any]]:
    """
    Функция загружает данные о финансовых транзакциях из JSON-файла
    """
    logger.debug(f'Начало загрузки данных из файла: {file_path}')

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            logger.info(f'Успешно открыт файл: {file_path}')

            data = json.load(file)
            logger.debug('JSON успешно загружен из файла')

            if isinstance(data, list):
                logger.info(f'Загружено {len(data)} операций из файла')
                return data

            logger.warning('Данные в файле не являются списком. Возвращаем пустой список')
            return []

    except FileNotFoundError:
        logger.error(f'Файл не найден: {file_path}')
        return []
    except json.JSONDecodeError as e:
        logger.error(f'Ошибка декодирования JSON: {str(e)}')
        return []
    except Exception as e:
        logger.error(f'Непредвиденная ошибка при чтении файла: {str(e)}')
        return []