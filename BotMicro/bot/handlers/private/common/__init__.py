from aiogram import Router

from .cancel import router as cancel_router

owners_router = Router()
owners_router.include_router(cancel_router)
