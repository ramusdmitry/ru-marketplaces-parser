from parser.base_parser import BaseParser
from parser.constants import TAGS


class WBParser(BaseParser):
    def __init__(self):
        super().__init__(name='WB', tags=TAGS)

    def get_product_price(self, driver: WebDriver) -> dict:
        result = {
            "discount_price": -1,
            "original_price": -1,
            "special_price": -1,
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