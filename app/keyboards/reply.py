from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           KeyboardButtonRequestChat)

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Админ-панель')
        ]
    ],
    resize_keyboard=True
)

chats_select_panel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="Чаты",
                request_chat=KeyboardButtonRequestChat(
                    request_id=2,
                    chat_is_channel=False,
                    request_title=True
                )
            )
        ],
        [
            KeyboardButton(text="🔙 Назад")
        ]
    ],
    resize_keyboard=True
)