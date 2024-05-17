from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import logging

from storage import db
from storage.db import session
from .models import User, Product, ProductPrice, UserProduct


# Функция для добавления или обновления продукта
def add_or_update_product(session: Session, user_id: int, username: str, product_name: str, url: str,
                          special_price: float, discount_price: float, original_price: float):
    try:
        # Поиск пользователя
        user = session.query(User).filter(User.user_id == user_id).first()
        if not user:
            logging.info(f"User with id {user_id} not found. Adding new user.")
            user = User(
                user_id=user_id,
                username=username,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            session.add(user)
            session.commit()  # Коммитим, чтобы получить ID пользователя

        # Поиск продукта
        product = session.query(Product).filter(Product.url == url).first()
        if not product:
            logging.info(f"Product with URL {url} not found. Adding new product.")
            product = Product(
                product_name=product_name,
                url=url,
                user_id=user.user_id,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            session.add(product)
            session.commit()  # Коммитим, чтобы получить ID продукта

        # Добавление новой цены продукта
        new_price = ProductPrice(
            product_id=product.id,
            special_price=special_price,
            discount_price=discount_price,
            original_price=original_price,
            checked_at=datetime.now()
        )
        session.add(new_price)

        # Проверка связи пользователя с продуктом
        user_product = session.query(UserProduct).filter(UserProduct.user_id == user_id,
                                                         UserProduct.product_id == product.id).first()
        if not user_product:
            user_product = UserProduct(
                user_id=user.user_id,
                product_id=product.id,
                created_at=datetime.now()
            )
            session.add(user_product)

        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        logging.error(f"An error occurred while adding or updating the product: {e}")
        raise


# Функция для удаления продукта
def delete_product(session: Session, product_id: int):
    try:
        product = session.query(Product).filter(Product.id == product_id).first()
        if not product:
            logging.info(f"Product with id {product_id} not found.")
            return

        session.delete(product)
        session.commit()
        logging.info(f"Product with id {product_id} has been deleted.")
    except SQLAlchemyError as e:
        session.rollback()
        logging.error(f"An error occurred while deleting the product: {e}")
        raise


# Функция для получения информации о продукте
def get_product(session: Session, product_id: int):
    try:
        product = session.query(Product).filter(Product.id == product_id).first()
        if not product:
            logging.info(f"Product with id {product_id} not found.")
            return None

        product_info = {
            "id": product.id,
            "product_name": product.product_name,
            "url": product.url,
            "created_at": product.created_at,
            "updated_at": product.updated_at,
            "prices": []
        }

        for price in product.prices:
            product_info["prices"].append({
                "yandex_price": price.yandex_price,
                "discount_price": price.discount_price,
                "original_price": price.original_price,
                "checked_at": price.checked_at
            })

        return product_info
    except SQLAlchemyError as e:
        logging.error(f"An error occurred while retrieving the product: {e}")
        return None


def get_products(session: Session):
    try:
        return session.query(Product).all()
    except SQLAlchemyError as e:
        logging.error(f"An error occurred while retrieving the products: {e}")
        return None

def get_urls(session: Session):
    try:
        products = session.query(Product).all()
        return [p.url for p in products]
    except SQLAlchemyError as e:
        logging.error(f"An error occurred while retrieving the products urls: {e}")
        return None