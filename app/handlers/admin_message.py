from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

import app.keyboards.builder as bkb
import app.keyboards.inline as ikb

from app.database.requests.admin.select import get_admins, get_admin
from app.database.requests.admin.delete import delete_admin
from app.database.requests.admin.add import set_admin

from app.states import AddAdmin

admin = Router()


@admin.message(CommandStart())
async def start_command(message: Message):
    await message.answer(f"Вы успешно авторизовались как администратор!",
                         reply_markup=ikb.admin_panel)


@admin.callback_query(F.data == "admins")
async def all_admins(callback: CallbackQuery):
    await callback.message.edit_text("<b>Текущие администраторы бота:</b>",
                                     reply_markup=await bkb.admins_cb())


@admin.callback_query(F.data == "add_admin")
async def add_admin(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("<b>Введите Telegram ID администратора:</b>",
                                     reply_markup=ikb.admin_cancel)

    await state.set_state(AddAdmin.tg_id)


@admin.message(AddAdmin.tg_id)
async def add_admin(message: Message, state: FSMContext):
    if message.text and message.text.isdigit():
        await set_admin(int(message.text))

        await message.answer("<b>Администратор успешно добавлен!</b>",
                             reply_markup=await bkb.admins_cb())

        await state.clear()

    else:
        await message.answer("<b>Введите корректный Telegram ID!</b>",
                             reply_markup=ikb.admin_cancel)


@admin.callback_query(F.data.startswith("admin_"))
async def admin_info_panel(callback: CallbackQuery):
    admin_id = int(callback.data.split("_")[1])
    admin_info = await get_admin(admin_id)

    await callback.message.edit_text(f"<b>Панель управления администратором №{admin_info.id}:</b>\n\n"
                                     f"<b>Telegram ID:</b> {admin_info.tg_id}\n\n"
                                     f"<b><i>Выберите действие:</i></b>",
                                     reply_markup=await bkb.edit_admin(admin_id))


@admin.callback_query(F.data.startswith("deleteadmin_"))
async def remove_admin(callback: CallbackQuery):
    admin_id = int(callback.data.split("_")[1])
    await delete_admin(admin_id)

    await callback.message.edit_text("<b>Администратор успешно удален!</b>",
                                     reply_markup=await bkb.admins_cb())



@admin.callback_query(F.data == "back")
async def back(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(f"Вы успешно авторизовались как администратор!",
                         reply_markup=ikb.admin_panel)

    await state.clear()
