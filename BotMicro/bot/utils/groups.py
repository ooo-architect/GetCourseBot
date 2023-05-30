from asyncio import gather

from aiogram import Bot
from aiogram.types import ChatInviteLink


async def kick_members_in_many_chats(
    user_ids: list[int],
    chat_ids: list[int],
    bot: Bot
) -> dict[int, list[int]]:
    """Return which members was kicked in which chats"""

    results = await gather(
        *[
            bot.ban_chat_member(chat_id, user_id)
            for user_id in user_ids
            for chat_id in chat_ids
        ],
        return_exceptions=True
    )
    
    kicked_members = {
        chat_id: [user_id for user_id, status in zip(
            user_ids, chat_results) if status == True]
        for chat_id, chat_results in zip(chat_ids, results)
    }
    return kicked_members


async def get_personal_invite_link(chat_id: int, bot: Bot) -> ChatInviteLink:
    chat = await bot.get_chat(chat_id)
    invite_link = await bot.create_chat_invite_link(
        chat_id=chat_id,
        name=chat.full_name,
        member_limit=1
    )
    return invite_link


async def get_personal_invite_links(chat_ids: list[int], bot: Bot) -> list[ChatInviteLink]:
    invite_links = await gather(
        *[
            get_personal_invite_link(chat_id, bot)
            for chat_id in chat_ids
        ],
        return_exceptions=True
    )
    invite_links = [
        link for link in invite_links if isinstance(link, ChatInviteLink)]
    return invite_links
