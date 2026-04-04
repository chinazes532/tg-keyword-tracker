from aiogram.fsm.state import State, StatesGroup


class AddAdmin(StatesGroup):
    tg_id = State()


class AddUserBot(StatesGroup):
    api_id = State()
    api_hash = State()
    phone_number = State()
    request_code = State()
    password = State()


class AddKeyword(StatesGroup):
    keyword = State()


class UpdateKeyword(StatesGroup):
    new_keyword = State()


class AddChat(StatesGroup):
    chat = State()