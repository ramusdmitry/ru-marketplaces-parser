import logging
import re
import time

from selenium import webdriver
from selenium.common import NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from parser.constants import TAGS
from parser.utils import get_driver, is_captcha_displayed
from storage import db
from storage.crud import add_or_update_product

logging.basicConfig(level=logging.INFO)


class BaseParser:

    def __init__(self, name: str, tags: dict = TAGS, url: str = ""):
        self.name = name
        assert name.upper() in ("YANDEX", "OZON", "WB", "MEGAMARKET")
        self.tags = tags[name.upper()]
        self.url = url
        self.driver = get_driver(url)

    def get_product_info(self):
        default_info = {
            "title": "",
            "description": "",
            "url": "",
            "original_price": -1,
            "discount_price": -1,
            "special_price": -1,
            "discount_percent": -1
        }

        if is_captcha_displayed(self.driver.current_url):
            self.close()
            return default_info

        try:
            product_info = {
                "title": self.get_product_title() if hasattr(self, 'get_product_title') else "",
                "description": self.get_product_description() if hasattr(self, 'get_product_description') else "",
                "url": self.url,
                "original_price": self.get_product_original_price() if hasattr(self,
                                                                               'get_product_original_price') else -1,
                "discount_price": self.get_product_discount_price() if hasattr(self,
                                                                               'get_product_discount_price') else -1,
                "special_price": self.get_product_special_price() if hasattr(self, 'get_product_special_price') else -1,
                "discount_percent": self.get_product_discount_percentage() if hasattr(self,
                                                                                      'get_product_discount_percentage') else -1
            }
        except Exception as e:
            logging.error(f"An error occurred while fetching product info: {e}")
            return default_info

        return product_info

    def get_product_title(self):
        pass

    def get_product_description(self):
        pass

    def get_product_original_price(self):
        pass

    def get_product_discount_price(self):
        pass

    def get_product_special_price(self):
        pass

    def get_product_discount_percentage(self):
        pass

    def get_product_prices(self):
        pass

    def get_elements(self, xpath: str, base_xpath: str = ""):
        if self.driver is None:
            raise WebDriverException("Driver is not initialized")
        if xpath == "":
            return ""
        try:
            elements = self.driver.find_elements(By.XPATH, f"{base_xpath}{xpath}")
            return [elem for elem in elements if len(elem.text) > 0]
        except NoSuchElementException:
            logging.error(f"{__name__}: Element not found for xpath: {xpath}")
            return ""
        except Exception as e:
            logging.error(f"{__name__}: An error occurred while fetching the element (xpath = {xpath}): {e}")
            return ""

    def get_element(self, xpath: str, base_xpath: str = "", delay: float = 0.0):
        if self.driver is None:
            raise WebDriverException("Driver is not initialized")
        if xpath == "":
            return ""
        try:
            if delay > 0:
                time.sleep(delay)
            return self.driver.find_element(By.XPATH, f"{base_xpath}{xpath}")
        except NoSuchElementException:
            logging.error(f"{__name__}: Element not found for xpath: {xpath}")
            return ""
        except Exception as e:
            logging.error(f"{__name__}: An error occurred while fetching the element (xpath = {xpath}): {e}")
            return ""

    def extract_prices(self, text: str):
        prices = []
        if self.name in ('yandex', 'wb'):
            pattern = re.compile(r'(\d[\d\s]*\d)')
            matches = pattern.findall(text)
            prices = [int(match.replace(' ', '').replace('\u2009', '')) for match in matches]
        return prices

    def extract_discount(self, text: str, parser_type: str = 'yandex'):
        discount_percent = -1
        if self.name in ('yandex', 'wb'):
            text = text.replace(' ', '').replace('-', '').replace('\u2009', '')
            pattern = re.compile(r'[ 0-9]+')
            matches = pattern.findall(text)
            discount_percent = matches[0]
        return int(discount_percent)

    def close(self):
        try:
            if self.driver:
                self.driver.quit()
        except Exception as e:
            logging.warning(f"{__name__}: failed to close webdriver: {e}")


if __name__ == '__main__':
    ### for test
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    yandex = BaseParser('yandex', TAGS)

    # url = 'https://market.yandex.ru/product--znachok-bag-you-metallicheskii-raskryvaiushchiisia-fbi/1789567142?sku=101862908508&uniqueId=30744390&do-waremd5=R8SXz21gPvShKF4swK40Lw&cpc=4AYLPk9tobgpiQs7RnVwOrJegQPNt1IO2FOzJK7RJqlmZBcBBWjJsu-U-AK3RX9c67iqTNUtpeAPyg6FGfB0Zr5-1n6i9LQt2YTu-UdP6TB6fLV286-NJlxUgC7iJOxreTennuu07zUu7hjkseViFtRH3dvn16a0PLXqILHhk7Xus-PCCfEinB3cETcmk3yO6RQPtBKQ-L8zAcN4dg8cgsOdjRZvGVhBmKEH8x-3kCshRLrv6GpfV3yjYremSg6CBnznKuxMTM47Whv4S_pa_8rTD5AYTu5VHYy73bnhKV0%2C'  # Замените на реальную ссылку товара
    url = 'https://market.yandex.ru/product--solntsezashchitnye-ochki-polaroid-polaroid-pld-6169-s-8cq-0f/1752955480?sku=101742224622&offerid=ESrtEkzxD3JmFDhc3Shq9w&cpc=4AYLPk9tobhlAh8tkozlooeMSIbhKzufg722yRDy3ees_Nmp3USges_vKzbBvG7-bJjWXF22KJW2tsfad9MVUWR0-oYaNKCIcVvSK4-6QZ83K0ak0WCU2bOK-I7xSYhQiwebXKey0wcg5bv_kJntb0jIOL05HJGi6hxiY5lcnMU5JXm9y1klOcMcoj9QXnpqsw9YpkmwEwinxF2bWROiQqdr06wvPGkaMBMLR58PR4iF6Is_mrdAQM1ajafDmGGkhm7iC9L5NjTTw1f9aGN1fCieh14ybAmkguxW5KhVLoc,&show-uid=17158825267474342936506005&uniqueId=3785520&lr=216&'
    # driver.get(url)
    product_info = yandex.get_product_info()

    add_or_update_product(session=db.session, **product_info, user_id=123, username="dimko")

    if product_info:
        print("Product Name:", product_info['product_name'])
        print("Special Price:", product_info['special_price'])
        print("Original Price:", product_info['original_price'])
        print("Discount Price:", product_info['discount_price'])
