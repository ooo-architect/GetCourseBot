from os import getenv

from aiogram import Router

from utils.env_parse import parse_bool

from .error import router as error_router
from .groups import groups_router
from .private import private_router

router = Router()
router.include_router(private_router)
router.include_router(groups_router)

if parse_bool(getenv('ENABLE_ERRORS_LOGS', 'false')):
    router.include_router(error_router)
