from aiogram import Router

from .connect_account import router as connect_account_router
from .group_menu import router as group_menu_router
from .menu import router as menu_router
from .start import router as start_router

owners_router = Router()
owners_router.include_router(start_router)
owners_router.include_router(connect_account_router)
owners_router.include_router(menu_router)
owners_router.include_router(group_menu_router)
