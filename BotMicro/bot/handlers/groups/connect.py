from aiogram import Bot, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from bot import messages
from models.account import Account
from models.group import Group

router = Router()


@router.message(Command('connect', ignore_mention=True))
@router.channel_post(Command('connect', ignore_mention=True))
async def connect_handler(message: Message, command: CommandObject, bot: Bot):
    if not command.args:
        return

    args = command.args.split()
    if len(args) != 2:
        return

    account = await Account.get_or_none(args[0])
    if account is None:
        return

    group = await Group.get_or_none(args[1])
    if group is None:
        return

    if message.sender_chat:
        connected_chat_id = message.sender_chat.id
    else:
        connected_chat_id = message.chat.id

    if connected_chat_id not in group.connected_chats:
        group.connected_chats.append(connected_chat_id)

    await group.save()
    await message.answer(messages.SUCCESS_CONNECT_CHAT)
