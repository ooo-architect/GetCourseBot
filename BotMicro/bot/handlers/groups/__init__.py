from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, Router
from aiogram.types import Message

from .connect import router as connect_router
from .members_control import router as members_control_router


class GroupChatMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if event.chat.type != 'private':
            return await handler(event, data)


groups_router = Router()
groups_router.include_router(connect_router)
groups_router.include_router(members_control_router)

groups_router.message.middleware(GroupChatMiddleware())
