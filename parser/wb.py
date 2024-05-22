import logging

from selenium.webdriver.remote.webelement import WebElement

from parser.base_parser import BaseParser


class WBParser(BaseParser):
    def __init__(self, url: str):
        super(WBParser, self).__init__(name='wb', url=url)

    def get_product_description(self):
        elem = self.get_element(self.tags["product_card"]["description"], delay=1)
        if isinstance(elem, WebElement):
            return elem.text
        return elem

    def get_product_title(self):
        elem = self.get_element(self.tags["product_card"]["title"], delay=1)
        if isinstance(elem, WebElement):
            return elem.text
        return elem

    def get_product_original_price(self):
        return self.get_prices().get('original_price')

    def get_product_discount_price(self):
        return self.get_prices().get('discount_price')

    def get_product_special_price(self):
        return self.get_prices().get('special_price')

    def get_product_discount_percentage(self):
        return self.get_prices().get('discount_percent')

    def get_prices(self) -> (str, str):
        tags = self.tags['product_card']['prices']['type_2']
        prices = {
            "original_price": -1,
            "discount_price": -1,
            "special_price": -1,
            "discount_percent": -1
        }
        base_xpath = '//p[@class="price-block__price-wrap "]'
        try:
            for key, xpath in tags.items():
                elems = self.get_elements(xpath)
                price_text = elems[0] if len(elems) > 0 else ''
                if isinstance(price_text, WebElement):
                    price_text = price_text.text
                extracted_prices = self.extract_prices(price_text)
                if extracted_prices:
                    prices[f"{key}_price"] = extracted_prices[0] if key != 'special' else min(extracted_prices)

            if prices["original_price"] > 0 and prices["discount_price"] > 0 and prices["discount_percent"] == -1:
                prices["discount_percent"] = round((1 - prices["discount_price"] / prices["original_price"]) * 100,
                                                   2)
        except Exception as e:
            logging.error(f"An error occurred while extracting prices: {e}")

        return prices


if __name__ == "__main__":

    urls = [
        'https://www.wildberries.ru/catalog/13489202/detail.aspx'
    ]

    for u in urls:
        wb_parser = WBParser(u)
        r = wb_parser.get_product_info()
        print(r)
