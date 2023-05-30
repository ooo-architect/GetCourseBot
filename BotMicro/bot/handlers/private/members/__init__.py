from aiogram import Router

from .start import router as start_router


members_router = Router()
members_router.include_router(start_router)
