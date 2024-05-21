from sqlalchemy import create_engine, Column, Integer, Text, DECIMAL, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    products = relationship("Product", back_populates="user")


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    prices = relationship("ProductPrice", back_populates="product")
    user = relationship("User", back_populates="products")


class ProductPrice(Base):
    __tablename__ = 'product_prices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    title = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    url = Column(Text, nullable=True)
    original_price = Column(DECIMAL(10, 2), nullable=True)
    discount_price = Column(DECIMAL(10, 2), nullable=True)
    special_price = Column(DECIMAL(10, 2), nullable=True)
    discount_percent = Column(DECIMAL(5, 2), nullable=True)
    checked_at = Column(TIMESTAMP, default=datetime.utcnow)
    product = relationship("Product", back_populates="prices")

class UserProduct(Base):
    __tablename__ = 'user_products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now)

DATABASE_URL = 'mysql+mysqlconnector://prices_user:password@localhost/prices_db'
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
