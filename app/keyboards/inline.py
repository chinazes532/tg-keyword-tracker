from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import config

admin_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🤖 ЮзерБот", callback_data="user_bot")],
        [InlineKeyboardButton(text="🎯 Ключевые слова", callback_data="keywords")],
        [InlineKeyboardButton(text="💬 Чаты", callback_data="chats")],
        [InlineKeyboardButton(text="👨‍💻 Администраторы", callback_data="admins")],
    ]
)

admin_cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back")]
    ]
)

user_bot_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="❌ Удалить", callback_data="delete_user_bot")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back")]
    ]
)

register_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="➕ Авторизовать ЮзерБота", callback_data="register")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back")]
    ]
)