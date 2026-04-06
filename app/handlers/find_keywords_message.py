from functools import partial

from aiogram import Bot
from telethon import TelegramClient, events

from app.database.requests.user_bot.select import get_user_bot_by_id
from app.database.requests.keyword.select import get_keyword_by_keyword, get_all_keywords
from app.database.requests.chat.select import get_all_chats, get_chat_by_tg_id
from app.database.requests.admin.select import get_admins


def normalize_tg_id(tg_id: int) -> int:
    str_id = str(tg_id)
    if not str_id.startswith("-100"):
        if str_id.startswith("-"):
            return int(f"-100{str_id[1:]}")
        else:
            return int(f"-100{str_id}")
    return tg_id


async def finder(event: events.NewMessage.Event, bot: Bot):
    chat = await event.get_chat()
    sender = await event.get_sender()  # Получаем автора сообщения

    if not chat:
        return

    chat_id = normalize_tg_id(chat.id)
    find_chat = await get_chat_by_tg_id(int(chat_id))

    if find_chat:
        message_text = event.message.message
        keywords = await get_all_keywords()
        admins = await get_admins()

        for keyword_obj in keywords:
            keyword = keyword_obj.keyword.lower()

            if keyword in message_text.lower():
                user_name = getattr(sender, 'first_name', 'Скрытый профиль')
                user_link = f"<a href='tg://user?id={sender.id}'>{user_name}</a>" if sender else "Пользователь"
                chat_title = getattr(chat, 'title', 'Группа')

                msg_link = ""
                if getattr(chat, 'username', None):
                    msg_link = f"\n\n<a href='https://t.me{chat.username}/{event.message.id}'>🔗 Перейти к сообщению</a>"

                text = (
                    f"🎯 <b>Найдено ключевое слово:</b> <code>{keyword}</code>\n"
                    f"👤 <b>Отправитель:</b> {user_link}\n"
                    f"📍 <b>Чат:</b> {chat_title}\n\n"
                    f"📝 <b>Сообщение:</b>\n<i>{message_text}</i>"
                    f"{msg_link}"
                )

                for admin in admins:
                    try:
                        await bot.send_message(
                            chat_id=admin.tg_id,
                            text=text,
                        )
                    except Exception as e:
                        print(f"Ошибка отправки админу {admin.tg_id}: {e}")

                break


async def setup_userbot(bot: Bot):
    user_bot = await get_user_bot_by_id()

    if not user_bot:
        return None

    client = TelegramClient('userbot', user_bot.api_id, user_bot.api_hash)
    await client.start()

    handler_with_bot = partial(finder, bot=bot)
    client.add_event_handler(handler_with_bot, events.NewMessage())

    return client