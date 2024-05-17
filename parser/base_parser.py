import logging
import re

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from parser.constants import TAGS
from storage import db
from storage.crud import add_or_update_product

logging.basicConfig(level=logging.INFO)

def extract_prices(text):
    # Регулярное выражение для поиска цен only for yandex
    # Пример: 'без: Вместо: 359₽499₽'
    pattern = re.compile(r'(\d[\d\s]*\d)')  # Захватывает числа, разделенные пробелами

    # Найти все совпадения
    matches = pattern.findall(text)

    prices = [int(match.replace(' ', '').replace('\u2009', '')) for match in matches]
    return prices


def get_driver():
    options = Options()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(options=options)

class BaseParser:

    def __init__(self, name: str, tags: dict):
        self.name = name
        if name.upper() in ("YANDEX", "OZON"):
            self.tags = tags[name.upper()]

    def get_product_price(self, driver: WebDriver) -> dict:
        ### Наверное стоит заменить на special_price, так как ozon_price, yandex_price это не оч
        result = {
            "discount_price": -1,  # Цена со скидкой от исходной цены
            "original_price": -1,  # Исходная цена
            "special_price": -1, # Цена вместе с Я.Пэй / Озон картой
        }

        price_tags = self.tags.get("prices")
        try:
            # Обработка текущей цены
            current_price_element = driver.find_element(By.XPATH, price_tags["current"])
            current_price_text = current_price_element.text
            current_prices = extract_prices(current_price_text)
            if current_prices:
                result["special_price"] = current_prices[0]

            # Обработка старой цены
            old_price_element = driver.find_element(By.XPATH, price_tags["old"])
            old_price_text = old_price_element.text
            old_prices = extract_prices(old_price_text)
            if old_prices:
                if len(old_prices) == 1:
                    result["original_price"] = result["discount_price"] = old_prices[0]
                elif len(old_prices) == 2:
                    result["original_price"] = max(old_prices)
                    result["discount_price"] = min(old_prices)

        except NoSuchElementException as e:
            logging.warning(f"{self.name}: Element not found: {e}")

        return result

    def get_product_name(self, driver: WebDriver) -> str:
        product_name = ""
        tag = self.tags["product_card"]["title"]
        try:
            product_name = driver.find_element(By.XPATH, tag).text
        except NoSuchElementException as e:
            logging.warning(e)
        return product_name

    def get_product_description(self, driver: WebDriver) -> str:
        product_description = ""
        tag = self.tags["product_card"]["description"]
        try:
            product_description = driver.find_element(By.XPATH, tag)
        except NoSuchElementException as e:
            logging.warning(e)
        return product_description

    def get_product_info(self, url: str):
        driver = get_driver()
        driver.get(url)
        if self.is_captcha_displayed(driver.current_url):
            driver.quit()
            return {}
        product_name = self.get_product_name(driver)
        prices = self.get_product_price(driver)

        driver.close()
        driver.quit()

        return {
            'product_name': product_name,
            'url': url,
            'original_price': prices.get('original_price', -1),
            'discount_price': prices.get('discount_price', -1),
            'special_price': prices.get('special_price', -1),
        }

    @staticmethod
    def is_captcha_displayed(url: str):
        if "captcha" in url:
            return True
        return False


if __name__ == '__main__':
    ### for test
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)


    yandex = BaseParser('yandex', TAGS)

    # url = 'https://market.yandex.ru/product--znachok-bag-you-metallicheskii-raskryvaiushchiisia-fbi/1789567142?sku=101862908508&uniqueId=30744390&do-waremd5=R8SXz21gPvShKF4swK40Lw&cpc=4AYLPk9tobgpiQs7RnVwOrJegQPNt1IO2FOzJK7RJqlmZBcBBWjJsu-U-AK3RX9c67iqTNUtpeAPyg6FGfB0Zr5-1n6i9LQt2YTu-UdP6TB6fLV286-NJlxUgC7iJOxreTennuu07zUu7hjkseViFtRH3dvn16a0PLXqILHhk7Xus-PCCfEinB3cETcmk3yO6RQPtBKQ-L8zAcN4dg8cgsOdjRZvGVhBmKEH8x-3kCshRLrv6GpfV3yjYremSg6CBnznKuxMTM47Whv4S_pa_8rTD5AYTu5VHYy73bnhKV0%2C'  # Замените на реальную ссылку товара
    url = 'https://market.yandex.ru/product--solntsezashchitnye-ochki-polaroid-polaroid-pld-6169-s-8cq-0f/1752955480?sku=101742224622&offerid=ESrtEkzxD3JmFDhc3Shq9w&cpc=4AYLPk9tobhlAh8tkozlooeMSIbhKzufg722yRDy3ees_Nmp3USges_vKzbBvG7-bJjWXF22KJW2tsfad9MVUWR0-oYaNKCIcVvSK4-6QZ83K0ak0WCU2bOK-I7xSYhQiwebXKey0wcg5bv_kJntb0jIOL05HJGi6hxiY5lcnMU5JXm9y1klOcMcoj9QXnpqsw9YpkmwEwinxF2bWROiQqdr06wvPGkaMBMLR58PR4iF6Is_mrdAQM1ajafDmGGkhm7iC9L5NjTTw1f9aGN1fCieh14ybAmkguxW5KhVLoc,&show-uid=17158825267474342936506005&uniqueId=3785520&lr=216&'
    # driver.get(url)
    product_info = yandex.get_product_info(url)

    add_or_update_product(session=db.session, **product_info, user_id=123, username="dimko")

    if product_info:
        print("Product Name:", product_info['product_name'])
        print("Special Price:", product_info['special_price'])
        print("Original Price:", product_info['original_price'])
        print("Discount Price:", product_info['discount_price'])
