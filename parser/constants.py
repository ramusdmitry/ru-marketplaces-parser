TAGS = {
    "YANDEX": {
        "prices": {
            "current": '//*[@data-auto="snippet-price-current"]', # special
            "old": '//*[@data-auto="snippet-price-old"]' #
        },
        "product_card": {
            "title": '//*[@data-auto="productCardTitle"]',
            "description": '//*[@itemprop="description"]'
        }
    },
    "MEGAMARKET": {
        "prices": {
            "current": '//*[@class="class="sales-block-offer-price__price-final"]', # span: class="sales-block-offer-price__price-final"
            "old": ''
        }
    },
    "WB": {
        "prices": {
            "special": "//span[@class='price-block__wallet-price']",
            "current": "//ins[@class='price-block__final-price wallet']",
            "old": "//del[@class='price-block__old-price']",
        },
        "product_card": {
            "title": "//h1[@class='product-page__title']",
        }
    }
}