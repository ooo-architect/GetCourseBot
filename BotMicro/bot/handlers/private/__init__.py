from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, Router
from aiogram.types import Message

from .members import members_router
from .owners import owners_router


class PrivateChatMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if event.chat.type == 'private':
            return await handler(event, data)


private_router = Router()
private_router.include_router(members_router)
private_router.include_router(owners_router)

private_router.message.middleware(PrivateChatMiddleware())
