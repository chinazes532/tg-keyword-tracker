from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests.admin.select import get_admins
from app.database.requests.keyword.select import get_all_keywords
from app.database.requests.chat.select import get_all_chats


async def admins_cb():
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="➕ Добавить администратора", callback_data="add_admin"))

    admins = await get_admins()
    for admin in admins:
        kb.row(InlineKeyboardButton(text=f"{admin.tg_id}", callback_data=f"admin_{admin.id}"))

    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back"))

    return kb.as_markup()


async def edit_admin(id: int):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="❌ Удалить", callback_data=f"deleteadmin_{id}"))
    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data=f"admins"))

    return kb.as_markup()


async def keywords_cb():
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="➕ Добавить слово", callback_data="add_keyword"))

    keywords = await get_all_keywords()
    for keyword in keywords:
        kb.row(InlineKeyboardButton(text=f"{keyword.keyword}", callback_data=f"keyword_{keyword.id}"))

    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back"))

    return kb.as_markup()


async def edit_keyword(id: int):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="✏️ Изменить", callback_data=f"update_keyword_{id}"))
    kb.row(InlineKeyboardButton(text="❌ Удалить", callback_data=f"delete_keyword_{id}"))
    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data=f"keywords"))

    return kb.as_markup()


async def chats_cb():
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="➕ Добавить чат", callback_data="add_chat"))

    chats = await get_all_chats()
    for chat in chats:
        kb.row(InlineKeyboardButton(text=f"{chat.title}", callback_data=f"chat_{chat.id}"))

    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back"))

    return kb.as_markup()


async def edit_chat(id: int):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="❌ Удалить", callback_data=f"delete_chat_{id}"))
    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data=f"chats"))

    return kb.as_markup()