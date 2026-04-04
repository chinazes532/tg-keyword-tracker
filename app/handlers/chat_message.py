from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

import app.keyboards.builder as bkb
import app.keyboards.inline as ikb
import app.keyboards.reply as rkb

from app.database.requests.chat.add import set_chat
from app.database.requests.chat.select import get_chat_by_id
from app.database.requests.chat.delete import delete_chat_by_id

from app.states import AddChat

chat = Router()


@chat.callback_query(F.data == "chats")
async def all_chats(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>Добавленные чаты:</b>",
        reply_markup=await bkb.chats_cb()
    )


@chat.callback_query(F.data == "add_chat")
async def add_chat_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    await callback.message.answer(
        "<b>Выберите чат:</b>",
        reply_markup=rkb.chats_select_panel
    )

    await state.set_state(AddChat.chat)


@chat.message(F.chat_shared, AddChat.chat)
async def check_chat(message: Message, state: FSMContext):
    chat_id = message.chat_shared.chat_id
    title = message.chat_shared.title
    request_id = message.chat_shared.request_id

    if request_id == 2:
        await set_chat(title, chat_id)

        await message.answer(
            f"Вы выбрали чат {title} с ID <code>{chat_id}</code>",
            reply_markup=ReplyKeyboardRemove()
        )

        await message.answer("✅ <b>Чат был успешно добавлен!</b>",
                             reply_markup=await bkb.chats_cb())

        await state.clear()


@chat.callback_query(F.data.startswith("chat_"))
async def check_chat(callback: CallbackQuery):
    chat_id = int(callback.data.split("_")[1])
    chat_info = await get_chat_by_id(chat_id)

    await callback.message.edit_text(
        f"<b>Панель управления чатом</b>\n\n"
        f"<b>Чат:</b> {chat_info.title}\n"
        f"<b>ID чата:</b> {chat_info.tg_id}\n\n"
        f"<i>Выберите действие:</i>",
        reply_markup=await bkb.edit_chat(chat_id)
    )


@chat.callback_query(F.data.startswith("delete_chat_"))
async def remove_chat(callback: CallbackQuery):
    chat_id = int(callback.data.split("_")[2])
    await delete_chat_by_id(chat_id)

    await callback.message.edit_text(
        "✅ <b>Чат был успешно удален!</b>",
        reply_markup=await bkb.chats_cb()
    )


@chat.message(F.text == "🔙 Назад")
async def admin_back_message(message: Message, state: FSMContext):
    await message.answer(
        "<b>Процесс добавления остановлен!</b>",
        reply_markup=ReplyKeyboardRemove()
    )

    await message.answer(
        "<b>Добавленные чаты:</b>",
        reply_markup=await bkb.chats_cb()
    )

    await state.clear()