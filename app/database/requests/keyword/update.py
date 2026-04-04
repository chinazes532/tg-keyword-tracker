from app.database.models import async_session
from app.database.models import KeyWord
from sqlalchemy import update


async def update_keyword(id: int, keyword: str):
    async with async_session() as session:
        await session.execute(
            update(KeyWord).where(KeyWord.id == id).values(keyword=keyword)
        )
        await session.commit()