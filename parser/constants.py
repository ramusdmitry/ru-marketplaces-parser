TAGS = {
    "YANDEX": {
        "product_card": {
            "title": '//*[@data-auto="productCardTitle"]',
            "description": '//*[@itemprop="description"]',
            "prices": {
                "type_1": {
                    "discount": "//span[@data-auto='price-value']",
                    "original": "//span[@class='']",
                },
                "type_2": {
                    "discount": '//span[@data-auto="snippet-price-current"]',
                    "original": '//span[@data-auto="snippet-price-old"]',
                },
                "type_3": {
                    "special": '//h3[@data-auto="snippet-price-current"]',
                    "discount": '//span[@data-auto="snippet-price-old"]',
                    "original": '//span[@data-auto="snippet-price-old"]',
                },
                "discount_percent": '//div[@data-auto="discount-badge"]',
                "price_subscribe": '//div[@data-zone-name="price-subscribe"]'
            },
        },
        "offer_card": "//div[@data-zone-name='cpa-offer']",
    },
    "WB": {
        "product_card": {
            "title": '//h1[@class="product-page__title"]',
            "description": '',
            "discount_percent": '',
            "price_subscribe": '',
            "prices": {
                "type_1": {
                    "discount": '//ins[@class="price-block__final-price"]',
                    "original": '//del[@class="price-block__old-price"]',
                },
                "type_2": {
                    "special": '//span[@class="price-block__wallet-price"]',
                    "discount": '//ins[@class="price-block__final-price wallet"]',
                    "original": '//del[@class="price-block__old-price"]',
                },

            },
        }

    },
    "MEGAMARKET": {
        "product_card": {
            "title": '',
            "description": '',
            "discount_percent": '',
            "price_subscribe": '',
            "prices": {
                "special": '',
                "discount": '//*[@class="class="sales-block-offer-price__price-final"]', # span: class="sales-block-offer-price__price-final"
                "original": '',
            },
        }

    }
}
