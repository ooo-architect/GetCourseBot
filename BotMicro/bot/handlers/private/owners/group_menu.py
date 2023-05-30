from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot import messages
from bot.callbacks.owner import (ConnectChatCallback, DisconnectChatCallback,
                                 EditInviteImageCallback,
                                 EditInviteTextCallback, GroupMenuCallback)
from bot.keyboards.owner import group_menu_kb, open_group_menu_kb
from bot.states.owner import EditInviteImageState, EditInviteTextState
from bot.utils.chats import get_chats
from bot.utils.deeplinks import get_private_deeplink
from get_course.utils.hooks import get_hook_add_link, get_hook_remove_link
from models.account import Account
from models.group import Group
from utils.logging import log_to_deta

router = Router()


@router.callback_query(GroupMenuCallback.filter())
async def open_group_menu_handler(
    query: CallbackQuery,
    callback_data: GroupMenuCallback,
    bot: Bot,
    state: FSMContext
):
    await query.answer()
    await state.clear()

    message = query.message
    if not message:
        return

    account = await Account.get_or_none(callback_data.account)
    if account is None:
        return

    group = await Group.get_or_none(callback_data.group)
    if group is None:
        return

    chats = await get_chats(group.connected_chats, bot)

    start_link = get_private_deeplink(account.domain, group.gid, '{uid}')
    add_link = get_hook_add_link(account.domain, group.gid)
    remove_link = get_hook_remove_link(account.domain, group.gid)

    await message.edit_text(
        messages.group_menu_header(group, start_link, add_link, remove_link),
        reply_markup=group_menu_kb(callback_data.account, group.key, chats)
    )


@router.callback_query(DisconnectChatCallback.filter())
async def disconnect_chat_handler(query: CallbackQuery, callback_data: DisconnectChatCallback, bot: Bot, state: FSMContext):
    await query.answer()
    await state.clear()

    message = query.message
    if not message:
        return

    account = await Account.get_or_none(callback_data.account)
    if account is None:
        return

    group = await Group.get_or_none(callback_data.group)
    if group is None:
        return

    if callback_data.chat_id in group.connected_chats:
        group.connected_chats.remove(callback_data.chat_id)

    await group.save()

    chats = await get_chats(group.connected_chats, bot)
    await message.edit_reply_markup(
        reply_markup=group_menu_kb(callback_data.account, group.key, chats)
    )


@router.callback_query(ConnectChatCallback.filter())
async def connect_chat_handler(query: CallbackQuery, callback_data: ConnectChatCallback, bot: Bot, state: FSMContext):
    await query.answer()
    await state.clear()

    message = query.message
    if not message:
        return

    await message.edit_text(
        messages.CHAT_CONNECT_INSTRUCTION.format(
            account=callback_data.account,
            group=callback_data.group
        ),
        reply_markup=open_group_menu_kb(
            callback_data.account, callback_data.group)
    )


@router.callback_query(EditInviteTextCallback.filter())
async def edit_invite_text_handler(query: CallbackQuery, callback_data: EditInviteTextCallback, state: FSMContext):
    await query.answer()

    message = query.message
    if not message:
        return

    await message.edit_text(
        messages.EDIT_INVITE_TEXT_INSTRUCTION,
        reply_markup=open_group_menu_kb(
            account=callback_data.account, group=callback_data.group)
    )

    await state.update_data(
        init_message=message.message_id,
        account=callback_data.account,
        group=callback_data.group
    )
    await state.set_state(EditInviteTextState.invite_text)


@router.message(EditInviteTextState.invite_text, F.text)
async def invite_text_handler(message: Message, bot: Bot, state: FSMContext):
    if not message.text:
        return

    data = await state.get_data()
    await state.clear()

    account = await Account.get_or_none(data['account'])
    if account is None:
        return

    group = await Group.get_or_none(data['group'])
    if group is None:
        return

    group.invite_text = message.text
    await group.save()

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data['init_message'],
        text=messages.SUCCESS_EDIT_INVITE_TEXT,
        reply_markup=open_group_menu_kb(data['account'], data['group'])
    )
    await message.delete()


@router.callback_query(EditInviteImageCallback.filter())
async def edit_invite_image_handler(query: CallbackQuery, callback_data: EditInviteImageCallback, state: FSMContext):
    await query.answer()

    message = query.message
    if not message:
        return

    await message.edit_text(
        messages.EDIT_INVITE_IMAGE_INSTRUCTION,
        reply_markup=open_group_menu_kb(
            account=callback_data.account, group=callback_data.group)
    )

    await state.update_data(
        init_message=message.message_id,
        account=callback_data.account,
        group=callback_data.group
    )
    await state.set_state(EditInviteImageState.invite_img)


@router.message(EditInviteImageState.invite_img, F.photo)
async def invite_image_handler(message: Message, bot: Bot, state: FSMContext):
    if not message.photo:
        return

    data = await state.get_data()
    await state.clear()

    account = await Account.get_or_none(data['account'])
    if account is None:
        return

    group = await Group.get_or_none(data['group'])
    if group is None:
        return

    photo = message.photo[-1]
    photo_data = await bot.download(photo)
    if not photo_data:
        return

    group.set_invite_image(photo_data)
    await group.save()

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data['init_message'],
        text=messages.SUCCESS_EDIT_INVITE_IMAGE,
        reply_markup=open_group_menu_kb(data['account'], data['group'])
    )
    await message.delete()


@router.message(EditInviteImageState.invite_img, Command('empty'))
async def empty_invite_image_handler(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    await state.clear()

    account = await Account.get_or_none(data['account'])
    if account is None:
        return

    group = await Group.get_or_none(data['group'])
    if group is None:
        return

    group.remove_invite_image()
    await group.save()

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data['init_message'],
        text=messages.SUCCESS_REMOVE_INVITE_IMAGE,
        reply_markup=open_group_menu_kb(data['account'], data['group'])
    )
    await message.delete()


@router.message(EditInviteImageState.invite_img)
async def other_invite_image_handler(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()

    await message.delete()
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data['init_message'],
        text=messages.INCORRECT_MESSAGE_TYPE,
        reply_markup=open_group_menu_kb(data['account'], data['group'])
    )
