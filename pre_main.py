import logging
import re

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from constants import TAGS
from storage import db
from storage.crud import add_or_update_product

### самая первая версия, это уже не имеет смысла, весь код запускается в worker.py

def extract_prices(text):
    # Регулярное выражение для поиска цен
    # Пример: 'без: Вместо: 359₽499₽'
    pattern = re.compile(r'(\d[\d\s]*\d)')  # Захватывает числа, разделенные пробелами

    # Найти все совпадения
    matches = pattern.findall(text)

    prices = [int(match.replace(' ', '').replace('\u2009', '')) for match in matches]
    return prices

def is_captcha_displayed(driver):
    if "captcha" in driver.current_url:
        return True
    return False

def get_product_price_card(driver):
    result = {
        "yandex_price": -1,  # Цена вместе с Я.Пэй
        "discount_price": -1,  # Цена со скидкой от исходной цены
        "original_price": -1,  # Исходная цена
    }

    tags = TAGS["prices"]
    try:
        # Обработка текущей цены
        current_price_element = driver.find_element(By.XPATH, f'//*[@data-auto="{tags["current"]}"]')
        current_price_text = current_price_element.text
        current_prices = extract_prices(current_price_text)
        if current_prices:
            result["yandex_price"] = current_prices[0]

        # Обработка старой цены
        old_price_element = driver.find_element(By.XPATH, f'//*[@data-auto="{tags["old"]}"]')
        old_price_text = old_price_element.text
        old_prices = extract_prices(old_price_text)
        if old_prices:
            if len(old_prices) == 1:
                result["original_price"] = result["discount_price"] = old_prices[0]
            elif len(old_prices) == 2:
                result["original_price"] = max(old_prices)
                result["discount_price"] = min(old_prices)

    except NoSuchElementException as e:
        logging.warning(f"Element not found: {e}")

    return result


def get_product_name(driver):
    product_name = ""
    tag = "productCardTitle"
    try:
        product_name = driver.find_element(By.XPATH, f'//*[@data-auto="{tag}"]').text
    except NoSuchElementException as e:
        logging.warning(e)
    return product_name


def get_product_info(url):
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    driver.get(url)

    if is_captcha_displayed(driver):
        driver.quit()
    # Дождаться загрузки страницы и пройти капчу, если она есть
    # time.sleep(10)  # Дайте достаточно времени для вручную пройденной капчи

    # Извлечение названия товара
    product_name = get_product_name(driver)

    # Извлечение цен
    prices = get_product_price_card(driver)

    # driver.quit()

    return {
        'product_name': product_name,
        'url': url,
        'yandex_price': prices.get('yandex_price', -1),
        'original_price': prices.get('original_price', -1),
        'discount_price': prices.get('discount_price', -1),
    }


if __name__ == "__main__":
    url = 'https://market.yandex.ru/product--znachok-bag-you-metallicheskii-raskryvaiushchiisia-fbi/1789567142?sku=101862908508&uniqueId=30744390&do-waremd5=R8SXz21gPvShKF4swK40Lw&cpc=4AYLPk9tobgpiQs7RnVwOrJegQPNt1IO2FOzJK7RJqlmZBcBBWjJsu-U-AK3RX9c67iqTNUtpeAPyg6FGfB0Zr5-1n6i9LQt2YTu-UdP6TB6fLV286-NJlxUgC7iJOxreTennuu07zUu7hjkseViFtRH3dvn16a0PLXqILHhk7Xus-PCCfEinB3cETcmk3yO6RQPtBKQ-L8zAcN4dg8cgsOdjRZvGVhBmKEH8x-3kCshRLrv6GpfV3yjYremSg6CBnznKuxMTM47Whv4S_pa_8rTD5AYTu5VHYy73bnhKV0%2C'  # Замените на реальную ссылку товара
    product_info = get_product_info(url)

    add_or_update_product(session=db.session, **product_info, user_id=123, username="dimko")

    if product_info:
        print("Product Name:", product_info['product_name'])
        print("Yandex.Pay Price:", product_info['yandex_price'])
        print("Original Price:", product_info['original_price'])
        print("Discount Price:", product_info['discount_price'])
