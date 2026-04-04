from app.database.models import async_session
from app.database.models import KeyWord
from sqlalchemy import select


async def get_all_keywords():
    async with async_session() as session:
        keywords = await session.scalars(select(KeyWord))
        return keywords


async def get_keyword_by_id(id: int):
    async with async_session() as session:
        keyword = await session.scalar(select(KeyWord).where(KeyWord.id == id))
        return keyword


async def get_keyword_by_keyword(keyword: str):
    async with async_session() as session:
        keyword = await session.scalar(select(KeyWord).where(KeyWord.keyword == keyword))
        return keyword
