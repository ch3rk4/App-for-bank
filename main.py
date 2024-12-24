from datetime import datetime
from typing import List, Optional, Tuple

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
            # Преобразуем загруженные данные в формат Transaction
            return [
                Transaction(
                    id=str(tr["id"]),
                    state=tr["state"],
                    date=datetime.fromisoformat(tr["date"].replace("Z", "+00:00")),
                    amount=float(tr["amount"]),
                    currency_name=tr["currency_name"],
                    currency_code=tr["currency_code"],
                    from_account=tr.get("from_", ""),
                    to_account=tr.get("to", ""),
                    description=tr["description"],
                )
                for tr in transactions
            ]
        elif file_type == 2:
            return read_transactions_csv(file_path)
        elif file_type == 3:
            return read_transactions_excel(file_path)
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла: {str(e)}")
        return None


def format_amount_and_currency(transaction: Transaction) -> Tuple[str, str]:
    """
    Форматирует сумму и валюту транзакции для вывода пользователю.
    """
    amount = str(transaction["amount"])
    currency = transaction["currency_name"]
    return amount, currency


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
            choice_input = input("\nПользователь: ").strip()
            if not choice_input.isdigit():
                print("Пожалуйста, введите число от 1 до 3")
                continue

            choice = int(choice_input)  # преобразуем строку в число
            if choice not in [1, 2, 3]:
                print("Пожалуйста, выберите число от 1 до 3")
                continue

            file_paths: dict[int, str] = {  # явно указываем типы ключей и значений словаря
                1: "data/operations.json",
                2: "data/transactions.csv",
                3: "data/transactions_excel.xlsx",
            }

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
                    "\nПрограмма: Отфильтровать список транзакций по типу операции в описании? Да/Нет\nПользователь: "
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
                        for tr in filtered_transactions:
                            amount, currency = format_amount_and_currency(tr)
                            print(f"{tr['date'].strftime('%d.%m.%Y')} {tr['description']}")
                            print(f"{tr['from_account']} -> {tr['to_account']}")
                            print(f"Сумма: {amount} {currency}\n")
                        print(f"{from_account} -> {to_account}")
                        print(f"Сумма: {amount} {currency}\n")

                break
            break

        except ValueError:
            print("Пожалуйста, введите корректное число")
            continue


if __name__ == "__main__":
    main()
