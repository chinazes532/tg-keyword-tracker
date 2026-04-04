from app.database.models import async_session
from app.database.models import KeyWord


async def set_keyword(keyword: str):
    async with async_session() as session:
        session.add(KeyWord(keyword=keyword))
        await session.commit()