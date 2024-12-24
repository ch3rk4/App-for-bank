from datetime import datetime
from typing import List, Optional

from src.finance_reader.readers import read_transactions_csv, read_transactions_excel
from src.finance_reader.types import Transaction
from src.transaction_processor import search_transactions
from src.utils import load_operations


def get_transactions_from_file(file_type: int, file_path: str) -> Optional[List[Transaction]]:
    """
    Получает список транзакций из файла в зависимости от его типа.
    """
    try:
        if file_type == 1:
            transactions = load_operations(file_path)
            # Преобразуем строковые даты в datetime объекты
            for transaction in transactions:
                if isinstance(transaction["date"], str):
                    transaction["date"] = datetime.strptime(transaction["date"].split(".")[0], "%Y-%m-%dT%H:%M:%S")
                # Также нужно правильно обработать поля from_ и from
                if "from_" in transaction:
                    transaction["from_account"] = transaction.pop("from_")
                if "to" in transaction:
                    transaction["to_account"] = transaction.pop("to")
            return transactions
        elif file_type == 2:
            return read_transactions_csv(file_path)
        elif file_type == 3:
            return read_transactions_excel(file_path)
        else:
            print("Неверный тип файла")
            return None
    except Exception as e:
        print(f"Ошибка при чтении файла: {str(e)}")
        return None


def filter_by_status(transactions: List[Transaction], status: str) -> List[Transaction]:
    """
    Фильтрует транзакции по статусу.
    """
    normalized_status = status.upper()
    return [t for t in transactions if t.get("state", "").upper() == normalized_status]


def main() -> None:
    """
    Основная функция программы, реализующая взаимодействие с пользователем
    и обработку транзакций.
    """
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    while True:
        print("\nВыберите необходимый пункт меню:")
        print("1. Получить информацию о транзакциях из JSON-файла")
        print("2. Получить информацию о транзакциях из CSV-файла")
        print("3. Получить информацию о транзакциях из XLSX-файла")

        try:
            choice = input("\nПользователь: ").strip()
            if not choice.isdigit() or int(choice) not in [1, 2, 3]:
                print("Пожалуйста, выберите число от 1 до 3")
                continue

            choice = int(choice)
            file_paths = {1: "data/operations.json", 2: "data/transactions.csv", 3: "data/transactions_excel.xlsx"}

            print(f"\nПрограмма: Для обработки выбран {['JSON', 'CSV', 'XLSX'][choice - 1]}-файл.")

            transactions = get_transactions_from_file(choice, file_paths[choice])
            if not transactions:
                print("Не удалось загрузить транзакции. Попробуйте другой файл.")
                continue

            while True:
                print("\nПрограмма: Введите статус, по которому необходимо выполнить фильтрацию.")
                print("Доступные для фильтровки статусы: EXECUTED, CANCELED")

                status = input("\nПользователь: ").upper()
                if status not in ["EXECUTED", "CANCELED"]:
                    print(f'\nПрограмма: Статус операции "{status}" недоступен.')
                    continue

                filtered_transactions = filter_by_status(transactions, status)
                print(f'\nПрограмма: Операции отфильтрованы по статусу "{status}"')

                sort_choice = input("\nПрограмма: Отсортировать операции по дате? Да/Нет\n\nПользователь: ").lower()
                if sort_choice in ["да", "y", "yes"]:
                    sort_direction = input(
                        "\nПрограмма: Отсортировать по возрастанию или по убыванию?\n\nПользователь: "
                    ).lower()
                    filtered_transactions.sort(
                        key=lambda x: x["date"],
                        reverse=(sort_direction.startswith("у") or sort_direction.startswith("d")),
                    )

                rub_only = input("\nПрограмма: Выводить только рублевые транзакции? Да/Нет\n\nПользователь: ").lower()
                if rub_only in ["да", "y", "yes"]:
                    filtered_transactions = [
                        t
                        for t in filtered_transactions
                        if t.get("operationAmount", {}).get("currency", {}).get("code") == "RUB"  # type: ignore
                    ]

                search_choice = input(
                    "\nПрограмма: Отфильтровать список транзакций по типу операции в описании? Да/Нет\n\nПользователь: "
                ).lower()
                if search_choice in ["да", "y", "yes"]:
                    print("\nПрограмма: Введите тип операции для поиска.")
                    print("Например: 'перевод', 'вклад', 'оплата' и т.д.")
                    search_word = input("\nПрограмма: ")
                    filtered_transactions = search_transactions(filtered_transactions, search_word)

                print("\nПрограмма: Распечатываю итоговый список транзакций...")
                if not filtered_transactions:
                    print("\nПрограмма: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
                else:
                    print(f"\nПрограмма: Всего банковских операций в выборке: {len(filtered_transactions)}\n")
                    for tr in filtered_transactions:
                        print(f"{tr['date'].strftime('%d.%m.%Y')} {tr['description']}")
                        from_account = tr.get("from_account", "")
                        to_account = tr.get("to_account", "")
                        amount = tr.get("operationAmount", {}).get("amount", "0")
                        currency = tr.get("operationAmount", {}).get("currency", {}).get("name", "")
                        print(f"{from_account} -> {to_account}")
                        print(f"Сумма: {amount} {currency}\n")

                break
            break

        except ValueError:
            print("Пожалуйста, введите корректное число")
            continue


if __name__ == "__main__":
    main()
