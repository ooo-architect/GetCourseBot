from datetime import datetime

from aiogram import Bot, Router
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated, Message
from deta import Deta
from deta._async.client import _AsyncBase

from models.group import Group
from models.member import Member

router = Router()


async def remove_member(bot: Bot, chat_id: int, user_id: int):
    # ban and unban to remove user from group but leave ability of come back
    await bot.ban_chat_member(chat_id, user_id, revoke_messages=True)
    await bot.unban_chat_member(chat_id, user_id)
    base: _AsyncBase = Deta().AsyncBase('MockRemoveLogs')
    await base.put({'time': datetime.now().isoformat(), 'chat_id': chat_id, 'user_id': user_id})


@router.message()
async def member_message_handler(message: Message, bot: Bot):
    if not message.from_user:
        return

    chat_id = message.chat.id
    user_id = message.from_user.id

    members = await Member.query(Member.user_id == user_id)
    if not members:
        return await remove_member(bot, chat_id, user_id)

    member = members.pop()

    groups = await Group.get_all()
    connected_groups = [
        group for group in groups if chat_id in group.connected_chats]
    for group in connected_groups:
        if member.uid in group.unchecked_members:
            return

    await remove_member(bot, chat_id, user_id)


@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def new_member_handler(event: ChatMemberUpdated, bot: Bot):
    chat_id = event.chat.id
    user_id = event.new_chat_member.user.id

    members = await Member.query(Member.user_id == user_id)
    if not members:
        return await remove_member(bot, chat_id, user_id)

    member = members.pop()

    groups = await Group.get_all()
    connected_groups = [
        group for group in groups if chat_id in group.connected_chats]
    for group in connected_groups:
        if member.uid in group.unchecked_members:
            return

    await remove_member(bot, chat_id, user_id)
