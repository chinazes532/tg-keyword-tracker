from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import app.keyboards.builder as bkb
import app.keyboards.inline as ikb

from app.database.requests.keyword.add import set_keyword
from app.database.requests.keyword.select import get_keyword_by_id
from app.database.requests.keyword.update import update_keyword
from app.database.requests.keyword.delete import delete_keyword_by_id

from app.states import AddKeyword, UpdateKeyword


keyword = Router()


@keyword.callback_query(F.data == "keywords")
async def all_keywords(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>Добавленные ключевые слова:</b>",
        reply_markup=await bkb.keywords_cb()
    )


@keyword.callback_query(F.data == "add_keyword")
async def add_keyword(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "<b>Введите ключевое слово для поиска:</b>",
        reply_markup=ikb.admin_cancel
    )

    await state.set_state(AddKeyword.keyword)


@keyword.message(AddKeyword.keyword)
async def check_keyword(message: Message, state: FSMContext):
    if message.text and len(message.text) <= 255:
        await set_keyword(message.text)

        await message.answer(
            "<b>Ключевое слово было успешно добавлено!</b>",
            reply_markup=await bkb.keywords_cb()
        )

        await state.clear()

    else:
        await message.answer(
            "<b>Ключевое слово должно быть текстом до 255 символов!</b>",
            reply_markup=ikb.admin_cancel
        )


@keyword.callback_query(F.data.startswith("keyword_"))
async def check_keyword(callback: CallbackQuery):
    keyword_id = int(callback.data.split("_")[1])
    keyword_info = await get_keyword_by_id(keyword_id)

    await callback.message.edit_text(
        f"<b>Панель управления ключевым словом</b>\n\n"
        f"<b>Ключевое слово:</b> <code>{keyword_info.keyword}</code>\n\n"
        f"<i>Выберите действие:</i>",
        reply_markup=await bkb.edit_keyword(keyword_id)
    )


@keyword.callback_query(F.data.startswith("update_keyword_"))
async def update_keyword_callback(callback: CallbackQuery, state: FSMContext):
    keyword_id = int(callback.data.split("_")[2])

    await callback.message.edit_text(
        "<b>Введите новое ключевое слово:</b>",
        reply_markup=ikb.admin_cancel
    )

    await state.set_state(UpdateKeyword.new_keyword)
    await state.update_data(id=keyword_id)


@keyword.message(UpdateKeyword.new_keyword)
async def check_new_keyword(message: Message, state: FSMContext):
    if message.text and len(message.text) <= 255:
        data = await state.get_data()

        id = data.get("id")

        await update_keyword(id, message.text)

        keyword_info = await get_keyword_by_id(id)

        await message.answer(
            f"<b>Панель управления ключевым словом</b>\n\n"
            f"<b>Ключевое слово:</b> <code>{keyword_info.keyword}</code>\n\n"
            f"<i>Выберите действие:</i>",
            reply_markup=await bkb.edit_keyword(id)
        )

        await state.clear()

    else:
        await message.answer(
            "<b>Ключевое слово должно быть текстом до 255 символов!</b>",
            reply_markup=ikb.admin_cancel
        )


@keyword.callback_query(F.data.startswith("delete_keyword_"))
async def remove_keyword(callback: CallbackQuery):
    keyword_id = int(callback.data.split("_")[2])
    await delete_keyword_by_id(keyword_id)

    await callback.message.edit_text(
        "✅ <b>Ключевое слово было успешно удалено!</b>",
        reply_markup=await bkb.keywords_cb()
    )