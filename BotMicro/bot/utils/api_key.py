from typing import Optional

from aiogram import Bot


async def get_api_key(chat_id: int, bot: Bot) -> Optional[str]:
    chat = await bot.get_chat(chat_id)
    return chat.pinned_message.text if chat.pinned_message else None
