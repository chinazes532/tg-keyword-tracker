from app.database.models import async_session
from app.database.models import UserBot
from sqlalchemy import delete, select, func


async def delete_first_user_bot():
    async with async_session() as session:
        subquery = select(func.min(UserBot.id)).scalar_subquery()
        await session.execute(delete(UserBot).where(UserBot.id == subquery))
        await session.commit()
