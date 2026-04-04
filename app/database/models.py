from typing import Annotated

from sqlalchemy import ForeignKey, String, BigInteger, Integer
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from config import config

engine = create_async_engine(url=config.database.sqlalchemy_url(),
                             echo=True)

async_session = async_sessionmaker(engine)

intpk = Annotated[int, mapped_column(primary_key=True)]


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Admin(Base):
    __tablename__ = 'admins'

    id: Mapped[intpk]
    tg_id: Mapped[int] = mapped_column(BigInteger)


class Chat(Base):
    __tablename__ = 'chats'

    id: Mapped[intpk]
    title: Mapped[str] = mapped_column(String(255))
    tg_id: Mapped[int] = mapped_column(BigInteger)


class KeyWord(Base):
    __tablename__ = 'keywords'

    id: Mapped[intpk]
    keyword: Mapped[str] = mapped_column(String(255))


class UserBot(Base):
    __tablename__ = 'userbot'

    id: Mapped[intpk]
    tg_id: Mapped[int] = mapped_column(BigInteger)
    phone_number: Mapped[str] = mapped_column(String(20))
    api_id: Mapped[int] = mapped_column(Integer)
    api_hash: Mapped[str] = mapped_column(String(50))


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
