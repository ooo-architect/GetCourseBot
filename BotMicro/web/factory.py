from os import getenv

from aiogram import Bot, Dispatcher
from deta import Deta
from fastapi import FastAPI

from web.routers import root_router
from web.stubs import BotStub, DispatcherStub, SecretStub


def get_webhook_secret() -> str:
    return getenv('DETA_SPACE_APP_MICRO_NAME', '') + getenv('DETA_PROJECT_KEY', '')[:4]


def create_app(deta: Deta, bot: Bot, dispatcher: Dispatcher) -> FastAPI:
    app = FastAPI(title='Bot')

    webhook_secret = get_webhook_secret()
    app.dependency_overrides.update({
        BotStub: lambda: bot,
        DispatcherStub: lambda: dispatcher,
        SecretStub: lambda: webhook_secret,
    })

    app.include_router(root_router)
    return app
