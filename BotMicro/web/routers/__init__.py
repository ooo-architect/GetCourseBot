from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from .info import info_router
from .members_hook import members_router
from .webhook import webhook_router

__all__ = ['root_router']


root_router = APIRouter()
root_router.include_router(webhook_router)
root_router.include_router(info_router)
root_router.include_router(members_router)


@root_router.get('/')
async def root():
    return RedirectResponse(url='/info')
