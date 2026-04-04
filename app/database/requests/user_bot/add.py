from app.database.models import async_session
from app.database.models import UserBot


async def set_user_bot(tg_id: int,
                       api_id: int,
                       api_hash: str,
                       phone_number: str):
    async with async_session() as session:
        session.add(UserBot(tg_id=tg_id,
                            api_id=api_id,
                            api_hash=api_hash,
                            phone_number=phone_number))
        await session.commit()