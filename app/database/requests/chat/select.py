from app.database.models import async_session
from app.database.models import Chat
from sqlalchemy import select


async def get_all_chats():
    async with async_session() as session:
        chats = await session.scalars(select(Chat))
        return chats


async def get_chat_by_id(id: int):
    async with async_session() as session:
        chat = await session.scalar(select(Chat).where(Chat.id == id))
        return chat


async def get_chat_by_tg_id(tg_id: int):
    async with async_session() as session:
        chat = await session.scalar(select(Chat).where(Chat.tg_id == tg_id))
        return chat