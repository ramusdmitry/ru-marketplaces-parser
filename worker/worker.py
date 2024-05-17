import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import parser.constants
from parser.base_parser import BaseParser
from storage import crud, db

# Настройки логирования
logging.basicConfig(level=logging.INFO)


# Функция для многопоточного парсинга
def multi_threaded_parsing(urls, max_workers=5):
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        yandex = BaseParser("YANDEX", parser.constants.TAGS)
        future_to_url = {executor.submit(yandex.get_product_info, url): url for url in urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
                if data:
                    results.append(data)
            except Exception as e:
                logging.error(f"Error occurred for URL {url}: {e}")
    return results

# Пример использования
if __name__ == "__main__":
    current_session = db.session
    urls = crud.get_urls(current_session)
    # urls = [
    #     "https://example.com/product1",
    #     "https://example.com/product2",
    #     "https://example.com/product3",
    #     # Добавьте больше URL-адресов для тестирования
    # ]
    #
    parsed_data = multi_threaded_parsing(urls, max_workers=5)
    for data in parsed_data:
        print(data)
