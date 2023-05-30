from aiogram.types import Chat, InlineKeyboardButton, InlineKeyboardMarkup

from bot.callbacks.owner import (AccountConnectionCallback,
                                 AccountMenuCallback, ConnectChatCallback,
                                 DisconnectChatCallback,
                                 EditInviteImageCallback,
                                 EditInviteTextCallback, GroupMenuCallback)
from models.group import Group


def start_account_connection_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='🔜 Меню администратора',
                callback_data=AccountConnectionCallback().pack()
            )
        ]
    ])


def open_account_menu_kb(account: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='⚙️ Меню',
                callback_data=AccountMenuCallback(account=account).pack()
            )
        ]
    ])


def account_menu_kb(account: str, groups: list[Group]) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=group.name,
                callback_data=GroupMenuCallback(account=account, group=group.key).pack()
            )
        ]
        for group in groups
    ]
    buttons.append([
        InlineKeyboardButton(
            text='🔃 Обновить список',
            callback_data=AccountMenuCallback(account=account).pack()
        )
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def group_menu_kb(account: str, group: str, chats: list[Chat]) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=f'📛 {chat.full_name}',
                callback_data=DisconnectChatCallback(account=account, group=group, chat_id=chat.id).pack()
            )
        ]
        for chat in chats
    ]
    buttons += [
        [
            InlineKeyboardButton(
                text='➕ Добавить чат',
                callback_data=ConnectChatCallback(account=account, group=group).pack()
            )
        ],
        [
            InlineKeyboardButton(
                text='📃 Изменить текст приглашения',
                callback_data=EditInviteTextCallback(account=account, group=group).pack()
            )
        ],
        [
            InlineKeyboardButton(
                text='🖼️ Изменить изображение приглашения',
                callback_data=EditInviteImageCallback(account=account, group=group).pack()
            )
        ],
        [
            InlineKeyboardButton(
                text='🔙 Назад',
                callback_data=AccountMenuCallback(account=account).pack()
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def open_group_menu_kb(account: str, group: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='🔙 Назад',
                callback_data=GroupMenuCallback(account=account, group=group).pack()
            )
        ]
    ])
