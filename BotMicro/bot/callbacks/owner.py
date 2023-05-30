from aiogram.filters.callback_data import CallbackData


class AccountConnectionCallback(CallbackData, prefix='account_connection'):
    pass


class AccountMenuCallback(CallbackData, prefix='account_menu'):
    account: str


class EditInviteTextCallback(CallbackData, prefix='edit_invite_text'):
    account: str
    group: str


class EditInviteImageCallback(CallbackData, prefix='edit_invite_image'):
    account: str
    group: str


class GroupMenuCallback(CallbackData, prefix='group_menu'):
    account: str
    group: str


class DisconnectChatCallback(CallbackData, prefix='disconnect_chat'):
    account: str
    group: str
    chat_id: int


class ConnectChatCallback(CallbackData, prefix='connect_chat'):
    account: str
    group: str
