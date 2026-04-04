import os
import sys
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

import redis.asyncio as aioredis

from app.filters.admin_filter import AdminProtect
from app.handlers.find_keywords_message import setup_userbot
from config import config

from app.handlers.admin_message import admin
from app.handlers.user_bot_message import user_bot
from app.handlers.key_words_message import keyword
from app.handlers.chat_message import chat

from app.database.models import create_db


async def main():
    print("Bot is starting...")

    redis = await aioredis.from_url(config.redis.redis_url)
    await create_db()

    bot = Bot(token=config.bot.bot_token,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=RedisStorage(redis))

    admin.message.middleware(AdminProtect())
    admin.callback_query.middleware(AdminProtect())
    user_bot.message.middleware(AdminProtect())
    user_bot.callback_query.middleware(AdminProtect())
    keyword.message.middleware(AdminProtect())
    keyword.callback_query.middleware(AdminProtect())
    chat.message.middleware(AdminProtect())
    chat.callback_query.middleware(AdminProtect())

    dp.include_router(admin)
    dp.include_router(user_bot)
    dp.include_router(keyword)
    dp.include_router(chat)

    user_client = await setup_userbot(bot)

    tasks = []
    tasks.append(dp.start_polling(bot, skip_updates=True))

    if user_client:
        print("Userbot найден и будет запущен.")
        tasks.append(user_client.run_until_disconnected())
    else:
        print("Userbot не настроен, пропускаем.")

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped!")
