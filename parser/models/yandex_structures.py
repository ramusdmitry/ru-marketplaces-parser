from dataclasses import dataclass


@dataclass
class Price:
    value: int = -1
    currency: str = 'RUR'


@dataclass
class YaBankPrice:
    price: Price
    type: str = 'ya-card'


@dataclass
class GreenPrice:
    price: Price
    type: str = 'ya-card'


@dataclass
class DiscountedPrice:
    price: Price
    discount: Price
    percent: int = -1


@dataclass
class PriceDetails:
    price: Price
    priceWithoutVat: Price
    greenPrice: GreenPrice = None
    discountedPrice: DiscountedPrice = None


@dataclass
class AdditionalPrice:
    priceType: str
    priceValue: int
