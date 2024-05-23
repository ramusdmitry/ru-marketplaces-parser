from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import logging

from .models import User, Product, ProductPrice

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

def get_products(session: Session):
    try:
        return session.query(Product).all()
    except SQLAlchemyError as e:
        logging.error(f"An error occurred while retrieving the products: {e}")
        return None


def get_users(session: Session):
    try:
        return session.query(User).all()
    except SQLAlchemyError as e:
        logging.error(f"An error occurred while retrieving the users: {e}")
        return None

def get_urls(session: Session):
    try:
        products = session.query(Product).all()
        return [p.url for p in products]
    except SQLAlchemyError as e:
        logging.error(f"An error occurred while retrieving the products urls: {e}")
        return None

def add_or_update_product(session: Session, user_id: int, title: str, description: str, url: str,
                          original_price: float, discount_price: float, special_price: float, discount_percent: float = 0.0, image_url: str = ''):
    try:
        user = session.query(User).filter(User.user_id == user_id).first()
        if not user:
            logging.info(f"User with id {user_id} not found. Adding new user.")
            user = User(
                user_id=user_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(user)
            session.commit()

        product = session.query(Product).filter(Product.url == url).first()
        if not product:
            logging.info(f"Product with URL {url} not found. Adding new product.")
            product = Product(
                product_name=title,
                url=url,
                image_url=image_url,
                user_id=user.user_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(product)
            session.commit()

        # Проверка изменений цен
        last_price = session.query(ProductPrice).filter(ProductPrice.product_id == product.id).order_by(ProductPrice.checked_at.desc()).first()
        if last_price:
            if last_price.original_price != original_price or last_price.discount_price != discount_price or last_price.special_price != special_price:
                notify_user = True
            else:
                notify_user = False
        else:
            notify_user = True

        # Добавление новой цены продукта
        new_price = ProductPrice(
            product_id=product.id,
            title=title,
            description=description,
            url=url,
            image_url=image_url,
            original_price=original_price,
            discount_price=discount_price,
            special_price=special_price,
            discount_percent=discount_percent,
            checked_at=datetime.utcnow()
        )
        session.add(new_price)
        session.commit()

        return notify_user
    except SQLAlchemyError as e:
        session.rollback()
        logging.error(f"An error occurred while adding or updating the product: {e}")
        raise

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
                "title": price.title,
                "description": price.description,
                "url": price.url,
                "original_price": price.original_price,
                "discount_price": price.discount_price,
                "special_price": price.special_price,
                "discount_percent": price.discount_percent,
                "checked_at": price.checked_at
            })

        return product_info
    except SQLAlchemyError as e:
        logging.error(f"An error occurred while retrieving the product: {e}")
        return None
