import re

TAGS = {
    "YANDEX": {
        "prices": {
            "current": "snippet-price-current",
            "old": "snippet-price-old"
        },
        "product_card": {
            "title": "productCardTitle"
        }
    }
}


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
