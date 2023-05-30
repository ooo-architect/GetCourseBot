import traceback
from os import getenv

from aiogram import Router
from aiogram.types.error_event import ErrorEvent

from utils.env_parse import parse_optional_int
from utils.logging import log_to_deta

router = Router()


@router.errors()
async def errors_handler(event: ErrorEvent):
    expire_after = parse_optional_int(getenv('ERROR_LOGS_EXPIRE_AFTER', ''))

    exception = event.exception
    stacktrace = traceback.format_exception(
        type(exception),
        exception,
        exception.__traceback__
    )
    with_traceback = ''.join(stacktrace)

    await log_to_deta(
        data={
            'exception': repr(exception),
            'with_traceback': with_traceback,
            'update': event.update.json()
        },
        expire_after=expire_after
    )
