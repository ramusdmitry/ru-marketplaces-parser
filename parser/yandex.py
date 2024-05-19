from dataclasses import dataclass, asdict

from selenium.webdriver.remote.webelement import WebElement

from base_parser import BaseParser
from constants import TAGS
from json import loads

from models.yandex_structures import PriceDetails


class YaParser(BaseParser):

    def __init__(self, url):
        super(YaParser, self).__init__(name='yandex', url=url)

    def get_product_description(self):
        tags = self.tags["product_card"]
        elem = self.get_element(tags["description"])
        if isinstance(elem, WebElement):
            return elem.text
        return elem

    def get_product_title(self):
        tags = self.tags["product_card"]
        elem = self.get_element(tags["title"])
        if isinstance(elem, WebElement):
            return elem.text
        return elem

    def get_price_details(self, data: dict):
        """

        :param data:
        :return:
        """
        price_details_raw = data.get("priceDetails")
        if not price_details_raw:
            return {}
        price_details = PriceDetails(**price_details_raw)
        price = data.get('price', -1)
        old_price = data.get('oldPrice', -1)

        """
        discountedPrice, как и greenPrice может и не быть
        вот какие связки есть:
        
        price + greenPrice + discountedPrice (три цены)
        price + greenPrice
        price + discountedPrice
        
        """

        return {
            **asdict(price_details),
            "price": price,  # текущая (зачёркнутая, есть всегда)
            "old_price": old_price  # старая, обычно равная price (зачёркнутая, есть не всегда)
        }

    def get_offer_card(self) -> dict:
        """
        Чтобы вернуть огромный json
        self.driver.find_element(By.XPATH, "//div[@data-zone-name='cpa-offer']").get_attribute('data-zone-data')
        :return:
        """
        tag = self.tags["offer_card"]
        elem = self.get_element(tag)
        if not elem:
            return {}
        json_data = elem.get_attribute('data-zone-data')
        data = loads(json_data)
        if not data:
            return {}
        return self.get_price_details(data)

    def get_product_original_price(self):
        """
        "price": 247
        :return:
        """
        return self.get_offer_card().get('price', -1)

    def get_product_price(self):
        """
        "price": {
          "value": 231,
          "currency": "RUR"
        },
        :return:
        """
        offer_card = self.get_offer_card()
        if not offer_card:
            return -1
        price = offer_card.get('price')
        if not price:
            return -1

        return price.get('value', -1)

    def get_product_discount_price(self) -> int:
        """
        "discountedPrice": {
          "price": {
            "value": 231,
            "currency": "RUR"
          },
          "discount": {
            "value": 16,
            "currency": "RUR"
          },
          "percent": 6
        }
        :return: value
        """
        offer_card = self.get_offer_card()
        if not offer_card:
            return -1

        discounted_price = offer_card.get('discountedPrice')
        if not discounted_price:
            return -1
        price = discounted_price.get('price')
        if not price:
            return -1
        return price.get('value', -1)

    def get_product_special_price(self) -> int:
        """
        "greenPrice": {
          "price": {
            "value": 229,
            "currency": "RUR"
          },
          "type": "ya-card"
        },
        :return: value
        """
        offer_card = self.get_offer_card()

        if not offer_card:
            return -1

        green_price = offer_card.get('greenPrice')
        if not green_price:
            return -1

        price = green_price.get('price')
        if not price:
            return -1

        return price.get('value', -1)

    def get_product_discount_percentage(self) -> int:
        offer_card = self.get_offer_card()
        if not offer_card:
            return -1

        discounted_price = offer_card.get('discountedPrice')
        if not discounted_price:
            return -1
        return discounted_price.get('percent', -1)



if __name__ == '__main__':

    urls = [
        "https://market.yandex.ru/product--solntsezashchitnye-ochki/1816465355?sku=101940647168&offerid=cxKFcC98w5RHxHe-DxDX9g&cpc=tg4KkW-wFZdbEls34SuNCQ-6OIp0cM461bvGrz7lr2JtymjW4YhECsT6nBEt8x4XwW5vD3azc-AKv7coES-aGx4Ld_K4VoGruuY3nIiocEiUV4EpH9eeGCCL5gmfzYEoBoqlN8IPtMl8uAX6JQzkRoOnM0WD-J2z_23d3I8_4Ikn0BDEvLXw8P3hpIAd-oYOCJxZOkcikV7TQQf591D9m8NKTK5mJphmc44ocETQ34DqVolfzGYM8x68ClS9lbcFjoDbrH9OU1XuaJ9zF9A5khS60Uiy42pxct1QYE7uK_E,&show-uid=17161242506704178846006011&uniqueId=6265044&lr=216&",
        "https://market.yandex.ru/product--gel-tint-dlia-gub-kiss-me-again/334398110?sku=100548401803&uniqueId=1167561&do-waremd5=kiJ1Pu8IvxjfEM0gU05xwg&sponsored=1&cpc=kAr-AWBSXoMvRGS3YqxhbZh7HkMSdPFBcelca61JO706XuUIqX_HiYiP6u-PJTH6RNkXeLPpNYQZdja6t52y2prGniwDbp3Ee3wPGZaCXeKiQWOvDNWXu2Viit_1psriXDBw7-DQ5nbNOliagmUoQtp6nnnedHJs3Y6EF9HXoNvKJaue9pbiB9JV0L5nRjSQVlh5fLJMMRGzVn1ulrVYfoNZGXy6_NZvR24xyd8hmFXSGRb8IopC9nJ33SQdXKEmHD9Xq9-jfvW0xR-E5Jb4eOl7dVnjfB5mP54G9NMk_ZY%2C",
        "https://market.yandex.ru/product--influence-beauty-blesk-dlia-gub-plexiglass-lip-gloss-ton-shade-05/1663269245?sku=101598313596&do-waremd5=qQQj7zd0a0xAo-_lhsciQg&showUid=17159736558560672185106002&uniqueId=993469&cpa=1&cpc=PRz2zu4wZJnHLMAhDovzql3cRPbyPHyY47KUTB4BgfB8URJ-_CH74BJ48gd5JEyTHPYvjq8i0qEIKwCNWb76EyNeAroVAiS_RWZodD5Yw8JjB8suN5lnhk9p-PlCN9u0Uyh24NwH_gH8DN-Z0ECogEN9Kl1ZDt5fhQD7KFWTrN10mQ-CNk1W5_jDJfoYSrmYuipRdw6xAkoxlEIxXjrBHqI9vCbFEZbpKYsEr6caVCLup-RPAhyRbV8h88kiX2JtTrknMilLOFB9G2v_lnV9WzXyyR4b_n8AAovsS6eBw7Y%2C&sponsored=1",
        "https://market.yandex.ru/product--blesk-dlia-gub-le-grand-volume/664040634?sku=100928907750&uniqueId=924574&do-waremd5=TkWAAtMswRA95y8XyphX9g"
    ]

    for u in urls:
        yandex_parser = YaParser(u)
        r = yandex_parser.get_product_info()
        print(r)
