import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, BigInteger, ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base, relationship


import os
from dotenv import load_dotenv

load_dotenv()
DB_NAME = os.getenv('DB_NAME')
DB_USERNAME = os.getenv('DB_USERNAME')
# DB_PORT = os.getenv('DB_PORT') -- test
# DB_HOST = os.getenv('DB_HOST') -- test
DB_PORT = '5432'
DB_HOST = "db"
DB_PASSWORD = os.getenv('DB_PASSWORD')
UKASSA_TEST_TOKEN = os.getenv('UKASSA_TEST_TOKEN')


DATABASE_URL = f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_async_engine(DATABASE_URL, echo=False)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(BigInteger, index=True, unique=True)
    tg_username = Column(String)
    balance = Column(Integer, default=0)

    applications = relationship("Application", back_populates="user")


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.chat_id'))
    business_type = Column(String)
    platform_type = Column(String)
    budget = Column(String)
    phone_number = Column(String)

    user = relationship("User", back_populates="applications")



async def get_session():
    async_session = AsyncSession(engine)
    async with async_session.begin():
        return async_session
