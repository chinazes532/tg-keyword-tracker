import os

from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

import app.keyboards.builder as bkb
import app.keyboards.inline as ikb

from app.database.requests.user_bot.add import set_user_bot
from app.database.requests.user_bot.select import get_user_bot_by_id
from app.database.requests.user_bot.delete import delete_first_user_bot

from app.utils.user_bot import get_user_bot

from app.states import AddUserBot

user_bot = Router()


@user_bot.callback_query(F.data == "user_bot")
async def user_bot_status(callback: CallbackQuery):
    user_bot_info = await get_user_bot_by_id()

    if user_bot_info:
        await callback.message.edit_text(
            f"<b>Панель управления ЮзерБотом</b>\n\n"
            f"<b>API ID:</b> {user_bot_info.api_id}\n"
            f"<b>API HASH:</b> {user_bot_info.api_hash}\n"
            f"<b>Номер телефона:</b> <code>{user_bot_info.phone_number}</code>\n\n"
            f"<i>Выберите действие:</i>",
            reply_markup=ikb.user_bot_panel
        )
    else:
        await callback.message.edit_text(
            "<b>ЮзерБот не зарегистрирован в боте 🥲</b>",
            reply_markup=ikb.register_panel
        )


@user_bot.callback_query(F.data == "register")
async def register_user(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "<b>Введите API ID:</b>",
        reply_markup=ikb.admin_cancel
    )

    await state.set_state(AddUserBot.api_id)


@user_bot.message(AddUserBot.api_id)
async def check_api_id(message: Message, state: FSMContext):
    if message.text and message.text.isdigit():
        await state.update_data(api_id=int(message.text))

        await message.answer(
            "<b>Введите API HASH:</b>",
            reply_markup=ikb.admin_cancel
        )

        await state.set_state(AddUserBot.api_hash)

    else:
        await message.answer("<b>API ID должен быть числом!</b>",
                             reply_markup=ikb.admin_cancel)


@user_bot.message(AddUserBot.api_hash)
async def check_api_hash(message: Message, state: FSMContext):
    if message.text and len(message.text) <= 50:
        await state.update_data(api_hash=message.text)

        await message.answer(
            "<b>Введите номер телефона:</b>",
            reply_markup=ikb.admin_cancel
        )

        await state.set_state(AddUserBot.phone_number)

    else:
        await message.answer("<b>API HASH должен быть текстом до 50 символов!</b>",
                             reply_markup=ikb.admin_cancel)


@user_bot.message(AddUserBot.phone_number)
async def check_api_phone_number(message: Message, state: FSMContext):
    if message.text and len(message.text) <= 20:
        await state.update_data(phone_number=message.text)

        data = await state.get_data()

        api_id = data.get("api_id")
        api_hash = data.get("api_hash")
        phone_number = data.get("phone_number")

        client = TelegramClient('userbot', api_id, api_hash)
        await client.connect()

        try:
            sent_code = await client.send_code_request(phone_number)
            await state.update_data(phone_code_hash=sent_code.phone_code_hash)

            await message.answer("<b>Введите код, который отправил вам Telegram:</b>",
                                 reply_markup=ikb.admin_cancel)

            await state.set_state(AddUserBot.request_code)
        except Exception as e:
            await message.answer(
                f"⚠️<b>Возникла ошибка</b>\n\n"
                f"<code>Проверьте корректность ввода данных для подключения и попробуйте снова</code>\n\n"
                f"<b>Детальный текст ошибки:</b>\n\n"
                f"<blockquote>{str(e)}</blockquote>",
                reply_markup=ikb.admin_cancel
            )

    else:
        await message.answer("<b>Номер телефона должен быть текстом до 20 символов!</b>",
                             reply_markup=ikb.admin_cancel)


@user_bot.message(AddUserBot.request_code)
async def check_request_code(message: Message, state: FSMContext):
    if message.text and message.text.isdigit():
        await state.update_data(request_code=int(message.text))

        data = await state.get_data()

        api_id = data.get("api_id")
        api_hash = data.get("api_hash")
        phone_number = data.get("phone_number")
        request_code = data.get("request_code")
        phone_code_hash = data.get("phone_code_hash")

        client = TelegramClient('userbot', api_id, api_hash)
        await client.connect()

        try:
            await client.sign_in(phone_number,
                                 request_code,
                                 phone_code_hash=phone_code_hash)

            await set_user_bot(
                tg_id=message.from_user.id,
                api_id=api_id,
                api_hash=api_hash,
                phone_number=phone_number,
            )

            await message.answer("<b>ЮзерБот успешно настроен!</b>",
                                 reply_markup=ikb.admin_cancel)

            await state.clear()

        except SessionPasswordNeededError:
            await message.answer("<b>Введите ваш пароль от 2ФА:</b>",
                                 reply_markup=ikb.admin_cancel)

            await state.set_state(AddUserBot.password)
        except Exception as e:
            await message.answer(
                f"⚠️<b>Возникла ошибка</b>\n\n"
                f"<code>Проверьте корректность ввода кода</code>\n\n"
                f"<b>Детальный текст ошибки:</b>\n\n"
                f"<blockquote>{str(e)}</blockquote>",
                reply_markup=ikb.admin_cancel
            )

    else:
        await message.answer(
            "<b>Код должен состоять из чисел!</b>",
            reply_markup=ikb.admin_cancel
        )


@user_bot.message(AddUserBot.password)
async def check_password(message: Message, state: FSMContext):
    if message.text:
        await state.update_data(password=message.text)

        data = await state.get_data()

        api_id = data.get("api_id")
        api_hash = data.get("api_hash")
        phone_number = data.get("phone_number")
        request_code = data.get("request_code")
        phone_code_hash = data.get("phone_code_hash")
        password = data.get("password")

        client = TelegramClient('userbot', api_id, api_hash)
        await client.connect()

        try:
            await client.sign_in(password=password)

            await set_user_bot(
                tg_id=message.from_user.id,
                api_id=api_id,
                api_hash=api_hash,
                phone_number=phone_number,
            )

            await message.answer("<b>ЮзерБот успешно настроен!</b>",
                                 reply_markup=ikb.admin_cancel)

            await state.clear()

        except Exception as e:
            await message.answer(
                f"⚠️<b>Возникла ошибка</b>\n\n"
                f"<code>Проверьте корректность ввода пароля 2ФА</code>\n\n"
                f"<b>Детальный текст ошибки:</b>\n\n"
                f"<blockquote>{str(e)}</blockquote>",
                reply_markup=ikb.admin_cancel
            )

    else:
        await message.answer("<b>Пароль должен быть в виде текстового сообщения:</b>",
                             reply_markup=ikb.admin_cancel)


@user_bot.callback_query(F.data == "delete_user_bot")
async def delete_user_bot(callback: CallbackQuery):
    client = await get_user_bot()

    if client:
        if await client.is_user_authorized():
            await client.log_out()

        await client.disconnect()

        if os.path.exists('userbot.session'):
            os.remove('userbot.session')

        await delete_first_user_bot()

        await callback.message.edit_text(
            "✅ <b>ЮзерБот полностью удален!</b>\n"
            "Сессия завершена, файл удален, запись в БД стерта.",
            reply_markup=ikb.admin_cancel
        )
    else:
        await callback.message.answer("Ошибка: ЮзерБот не найден в базе.")
