from telethon import TelegramClient
from app.database.requests.user_bot.select import get_user_bot_by_id


async def get_user_bot():
    user_bot = await get_user_bot_by_id()
    client = TelegramClient('userbot', user_bot.api_id, user_bot.api_hash)

    if not client.is_connected():
        await client.connect()

    return client


async def get_user_bot_data():
    user_bot = await get_user_bot_by_id()

    return user_bot.api_id, user_bot.api_hash