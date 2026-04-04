from app.database.models import async_session
from app.database.models import UserBot
from sqlalchemy import select


async def get_user_bot_by_id():
    async with async_session() as session:
        result = await session.execute(select(UserBot))
        return result.scalar()