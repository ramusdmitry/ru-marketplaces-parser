from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

# Создание базы данных и таблиц
DATABASE_URL = 'mysql+mysqlconnector://prices_user:password@localhost/prices_db'
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

