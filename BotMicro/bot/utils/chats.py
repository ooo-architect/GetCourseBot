from asyncio import gather

from aiogram import Bot
from aiogram.types import Chat


async def get_chats(chat_ids: list[int], bot: Bot) -> list[Chat]:
    chats = await gather(
        *[
            bot.get_chat(chat_id)
            for chat_id in chat_ids
        ],
        return_exceptions=False
    )
    return [chat for chat in chats if isinstance(chat, Chat)]
