import json
from typing import Callable, Optional, Any


# Функция для чтения данных из файла
def read_data(filename: str) -> Optional[list[dict[str, str]]]:
    """
      Получает данные справочника из файла.

      Parameters:
          filename (str): Имя файла в котором содержится справочник.

      Returns:
          data (list[dict[str, str]): Список всех записей из справочника
      """
    try:
        with open(filename, 'r') as file:
            data: list[dict] = json.load(file)
        return data
    except FileNotFoundError:
        return []


# Функция для записи данных в файл
def write_data(filename: str, data: list[dict[str, str]]) -> None:
    """
      Записывает данные справочника в файл.

      Parameters:
          filename (str): Имя файла в котором содержится справочник.
          data (list[dict[str, str]): Список всех записей.

      Returns:
          None
      """
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


# Функция для вывода записей постранично
def display_records(records: list[dict[str, str]], page_size: int, page_number: int) -> None:
    """
      Отображает записи из справочника.

      Parameters:
          records (list[dict[str, str]): Все записи из справочника в виду списка словарей.
          page_size (int): Количество страниц.
          page_number (int): Номер страницы справочника.

      Returns:
          None
      """
    start_index: int = (page_number - 1) * page_size
    end_index: int = start_index + page_size
    line: str = '+-{}-+-{}-+-{}-+-{}-+-{}-+-{}-+-{}-+'.format(
        '-' * 4,
        '-' * 20,
        '-' * 20,
        '-' * 20,
        '-' * 20,
        '-' * 15,
        '-' * 15
    )
    print(line)

    print(
        '| {:^4} | {:^20} | {:^20} | {:^20} | {:^20} | {:^15} | {:^15} |'.format(
            "№",
            "First Name",
            "Last Name",
            "Middle Name",
            "Organization",
            'Work phone',
            'Personal phone'
        )
    )
    print(line)

    for record in records[start_index:end_index]:
        print(
            "| {:^4} | {:^20} | {:^20} | {:^20} | {:^20} | {:^15} | {:^15} |".format(
                records.index(record) + 1,
                record['first_name'],
                record['last_name'],
                record['middle_name'],
                record['organization'],
                record['work_phone'],
                record['personal_phone']
            )
        )
        print(line)


# Функция для добавления новой записи
def add_record(records: list[dict[str, str]], record_data: dict[str, str]) -> None:
    """
      Добавляет запись в справочник.

      Parameters:
          records (list[dict[str, str]): Все записи из справочника в виду списка словарей.
          record_data (dict[str, str]): Данные для добавления записи

      Returns:
          None
      """
    records.append(record_data)


def change_record(records: list[dict[str, str]],
                  record_number: int,
                  record_to_change_data: dict[str, str]) -> Optional[dict[str, str]]:
    """
      Изменяет запись в справочнике.

      Parameters:
          records (list[dict[str, str]): Все записи из справочника в виду списка словарей.
          record_number (int): Номер записи для изменения.
          record_to_change_data (dict[str, str]): Данные по которым обновляется запись.

      Returns:
          record (dict[str, str]): Словарь с обновленное информацией о записи.
      """
    try:
        record: dict[str, str] = records[record_number - 1]
        if record_to_change_data['first_name']:
            record['first_name'] = record_to_change_data['first_name']

        if record_to_change_data['last_name']:
            record['last_name'] = record_to_change_data['last_name']

        if record_to_change_data['middle_name']:
            record['middle_name'] = record_to_change_data['middle_name']

        if record_to_change_data['organization']:
            record['organization'] = record_to_change_data['organization']

        if record_to_change_data['work_phone']:
            record['work_phone'] = record_to_change_data['work_phone']

        if record_to_change_data['personal_phone']:
            record['personal_phone'] = record_to_change_data['personal_phone']

        return record

    except IndexError:
        print('Enter valid number of record')


def search_record(records: list[dict[str, str]], sort_params: str) -> Optional[list[dict[str, str]]]:
    """
      Находит запись/записи в справочнике по критерию/критериям.

      Parameters:
          records (list[dict[str, str]): Все записи из справочника в виду списка словарей.
          sort_params (str): Перечисление номеров критериев поиска в виде строки.

      Returns:
          filtered_records (list[dict[str, str]]): Список словарей с найденное информацией
                                                   из справочника.
      """
    filter_functions: dict[str, Callable[[dict, str], bool]] = {
        '1': lambda record, value: record['first_name'] == value,
        '2': lambda record, value: record['last_name'] == value,
        '3': lambda record, value: record['middle_name'] == value,
        '4': lambda record, value: record['organization'] == value,
        '5': lambda record, value: record['work_phone'] == value,
        '6': lambda record, value: record['personal_phone'] == value,
    }

    filtered_records = records

    for param in sort_params.split():
        if param in filter_functions:
            value = input(f"Input a value for parameter {param}: ")
            filtered_records = list(
                filter(lambda x: filter_functions[param](x, value), filtered_records))

            return filtered_records

        else:
            print(f"Invalid parameter: {param}")
            break


def delete_record(records: list[dict[str, str]], record_number: int) -> None:
    """
      Удаляет запись из справочника по ее номеру.

      Parameters:
          records (list[dict[str, str]): Все записи из справочника в виду списка словарей.
          record_number (str): Номер удаляемой записи.

      Returns:
          None
      """
    del records[record_number-1]


# Основная функция
def main():
    while True:
        data_filename = 'phonebook.json'
        records = read_data(data_filename)

        print("\nPhonebook Menu:")
        print("1. Display Records")
        print("2. Add Record")
        print("3. Change Record")
        print("4. Find Record")
        print("5. Delete Record")
        print("6. Exit")
        choice = input("Select a number of option: ")

        if choice == '1':
            page_size = 5  # Количество записей на странице
            total_pages = (len(records) + page_size - 1) // page_size

            try:
                page_number = int(input(f"Enter page number (1 - {total_pages}): "))
                if 1 <= page_number <= total_pages:
                    display_records(records, page_size, page_number)
                else:
                    print("Invalid page number!")

            except ValueError:
                print('Enter a number of page!')

        elif choice == '2':
            record_data: dict[str, str] = {
                'first_name': input("First Name: "),
                'last_name': input("Last Name: "),
                'middle_name': input("Middle Name: "),
                'organization': input("Organization: "),
                'work_phone': input("Work Phone: "),
                'personal_phone': input("Personal Phone: ")
            }

            add_record(records, record_data)
            write_data(data_filename, records)

            print("Record added successfully!")

        elif choice == '3':
            change_item = int(input("What you want to change (tap a number): "))

            print("Input new values (if you dont want to change some item press enter): ")
            record_data_to_change: dict[str, str] = {
                'first_name': input("First Name: "),
                'last_name': input("Last Name: "),
                'middle_name': input("Middle Name: "),
                'organization': input("Organization: "),
                'work_phone': input("Work Phone: "),
                'personal_phone': input("Personal Phone: ")
            }

            changed_record = change_record(records, change_item, record_data_to_change)
            write_data(data_filename, records)

            if changed_record:
                print("Changes added:")
                for key, value in changed_record.items():
                    print(f"{key} - {value}")

        elif choice == '4':
            print("By what parameter need to find record: ")
            print("1. First Name")
            print("2. Last Name")
            print("3. Middle Name")
            print("4. Organization")
            print("5. Work_phone")
            print("6. Personal_phone")
            sort_param = input("Select numbers of parameter to search splited by spaces: ")

            filtered_records = search_record(records, sort_param)

            print(filtered_records)

        elif choice == '5':
            number = int(input("Select a number of record to delete: "))

            delete_record(records, number)
            write_data(data_filename, records)

            print(f"Record {number} deleted")

        elif choice == '6':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please select again.")


if __name__ == "__main__":
    main()
