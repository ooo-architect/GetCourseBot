from aiogram.fsm.state import State, StatesGroup


class AccountConnectionState(StatesGroup):
    domain = State()
    api_key = State()


class EditInviteTextState(StatesGroup):
    invite_text = State()


class EditInviteImageState(StatesGroup):
    invite_img = State()
