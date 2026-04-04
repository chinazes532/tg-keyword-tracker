from app.database.models import async_session
from app.database.models import Chat
from sqlalchemy import delete


async def delete_chat_by_id(id: int):
    async with async_session() as session:
        await session.execute(delete(Chat).where(Chat.id == id))
        await session.commit()