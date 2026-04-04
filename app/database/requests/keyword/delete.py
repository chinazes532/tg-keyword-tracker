from app.database.models import async_session
from app.database.models import KeyWord
from sqlalchemy import delete


async def delete_keyword_by_id(id: int):
    async with async_session() as session:
        await session.execute(delete(KeyWord).where(KeyWord.id == id))
        await session.commit()