import os
import json
import time

import requests


https_head = "https://"
country_ip_request = "https://ip-api.io/json/"


def main():
    user_input: bool = True

    while user_input:
        os.system("clear")
        print_menu()
        user_menu_input = input()
        os.system("clear")
        try:
            user_menu_input = int(user_menu_input)
            user_input = handle_menu(user_menu_input)
        except ValueError:
            pass


def handle_menu(user_menu_input: int) -> bool:
    """
    Handles user requests (int number from 1 to 7)
    :param user_menu_input: user request
    :type user_menu_input: int
    :returns: boolean value
    (True if user wants to continue using program and False if not)
    """

    if user_menu_input == 1:
        urls_dict = get_urls_from_file()
        if urls_dict is not False:
            print("Проверка доступности ресурсов")
            print("Страна проверки:", get_country_ip(), "\n")
            for category in urls_dict:
                temp_counter = 0
                urls_list = urls_dict[category]
                results = check(urls_list)
                for result in results:
                    if result[0] == "✅":
                        temp_counter += 1
                print(temp_counter, "/", len(urls_list), "\n")
            print("\nВведите что угодно чтобы продолжить")
            input()
        else:
            print("Файл пуст.")
            time.sleep(3)
        return True

    if user_menu_input == 2:
        print("Введите URL")
        input_url = input()
        print("Проверка доступности ресурса...")
        print("Страна проверки:", get_country_ip(), "\n")
        result = check(input_url)
        print("\nВведите что угодно чтобы продолжить")
        input()
        return True

    if user_menu_input == 3:
        print("Введите название категории")
        _ = add_new_category(get_urls_from_file(), input())
        time.sleep(3)
        return True

    if user_menu_input == 4:
        print("Введите название категории")
        _ = delete_category(get_urls_from_file(), input())
        time.sleep(3)
        return True

    if user_menu_input == 5:
        print("Введите категорию")
        input_cat = input()
        print("Введите URL")
        input_url = input()
        _ = add_new_url(get_urls_from_file(), input_cat, input_url)
        time.sleep(3)
        return True

    if user_menu_input == 6:
        print("Введите категорию")
        input_cat = input()
        print("Введите URL")
        input_url = input()
        _ = delete_url(get_urls_from_file(), input_cat, input_url)
        time.sleep(3)
        return True

    if user_menu_input == 7:
        return False

    else:
        print("Некорректный ввод")
        time.sleep(3)
        return True


def print_menu():
    """
    Prints main menu of program
    """

    print("Availability Checker v0.17.4.20\n")
    print("Выберите нужное действие:")
    print("1 - Проверить доступность ресурсов из файла")
    print("2 - Ввести URL и проверить доступность")
    print("3 - Добавить новую категорию сайтов")
    print("4 - Удалить категорию сайтов")
    print("5 - Добавить URL в категорию")
    print("6 - Удалить URL")
    print("7 - Закрыть программу")


def save_urls(urls_dict: dict) -> bool:
    """
    Saves urls dictionary to json file
    :param urls_dict:
    :type urls_dict: dict
    :returns: boolean value (true if saving was success and false if not)
    """

    if isinstance(urls_dict, dict):
        try:
            with open('urls.json', 'w') as f:
                json.dump(urls_dict, f)
            return True
        except FileNotFoundError:
            return False
    else:
        return False


def get_urls_from_file() -> dict or False:
    """
    Loads urls dictionary from json file
    :returns: urls dictionary if loading was success and False if not
    """

    try:
        with open('urls.json', 'r') as f:
            urls_dict = json.load(f)
        return urls_dict
    except FileNotFoundError:
        return False


def get_url_categories(urls_dict: dict) -> list:
    """
    Get categories of urls dictionary
    :param urls_dict: dictionary of urls for checking
    :type urls_dict: dict
    :returns: categories of urls from urls dictionary
    """

    return list(urls_dict.keys())


def add_new_category(urls_dict: dict, category: str) -> bool:
    """
    Adds category to urls dictionary
    :param urls_dict: dictionary of urls for checking
    :param category: category of urls for adding
    :type urls_dict: dict
    :type category: str
    :returns: boolean value (true if adding was success and false if not)
    """

    if category in urls_dict:
        print("Категория уже существует.")
        return False
    urls_dict[category] = []
    save_urls(urls_dict)
    print("Категория успешно добавлена")
    return True


def delete_category(urls_dict: dict, category: str) -> bool:
    """
    Deletes category from urls dictionary
    :param urls_dict: dictionary of urls for checking
    :param category: category of urls for deleting
    :type urls_dict: dict
    :type category: str
    :returns: boolean value (true if deleting was success and false if not)
    """

    if category not in urls_dict:
        print("Такой категории не существует")
        return False
    del urls_dict[category]
    print("Категория успешно удалена")
    save_urls(urls_dict)
    return True


def add_new_url(urls_dict: dict, category: str, url: str) -> bool:
    """
    Adds url to urls dictionary
    :param urls_dict: dictionary of urls for checking
    :param category: category of urls for adding
    :param url: url that will be added
    :type urls_dict: dict
    :type category: str
    :type url: str
    :returns: boolean value (true if adding was success and false if not)
    """

    if category not in urls_dict:
        add_new_category(urls_dict, category)
        print("Данной категории не существовало, но она была создана.")
        return False
    if url in urls_dict[category]:
        print("Данный URL уже есть в этой категории")
        return False
    urls_dict[category].append(url)
    save_urls(urls_dict)
    print("URL успешно добавлен")
    return True


def delete_url(urls_dict: dict, category: str, url: str) -> bool:
    """
    Deletes url from urls dictionary
    :param urls_dict: dictionary of urls for checking
    :param category: category of urls for deleting
    :param url: url that will be deleted
    :type urls_dict: dict
    :type category: str
    :type url: str
    :returns: boolean value (true if deleting was success and false if not)
    """

    if category not in urls_dict:
        print("Данной категории не существует")
        return False
    if url not in urls_dict[category]:
        print("В данной категории нет такого URL")
        return False
    urls_dict[category].pop(url)
    save_urls(urls_dict)
    print("URL успешно удален")
    return True


def check(urls_list: list) -> list:
    """
    Checks selected urls for their availability
    :param urls_list: url(s) list for checking
    :type urls_list: list
    :returns: list with availability status of site(s) and site url(s)
    """

    result = []
    for url in urls_list:
        if isinstance(urls_list, str):
            url = urls_list
        try:
            requests.get(https_head + url, stream=True,
                         allow_redirects=False, timeout=1)
            print("✅", url)
            result.append(("✅", url))
        except Exception:
            print("❌", url)
            result.append(("❌", url))
        if isinstance(urls_list, str):
            break
    return result


def get_country_ip() -> str:
    """
    Gets country flag by ip via api of ip-api.io service
    :returns: emoji with flag of user's country
    """

    return (requests.get(country_ip_request).json())['emojiFlag']


if __name__ == "__main__":
    main()
