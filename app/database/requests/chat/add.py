from app.database.models import async_session
from app.database.models import Chat


async def set_chat(title: str, tg_id: int):
    async with async_session() as session:
        session.add(Chat(title=title, tg_id=tg_id))
        await session.commit()