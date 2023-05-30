from datetime import datetime
from typing import Optional

from aiohttp import ClientSession
from pydantic import BaseModel

from get_course.utils.exceptions import (FiltersRequired,
                                         GetCourseApiException, IncorrectDate,
                                         IncorrectStatus, KeyNotSpecified,
                                         UnauthorizedRequest, UnknownException)


GC_API_URL = 'https://{domain}/pl/api/account'


class GCGroup(BaseModel):
    id: str
    name: str
    last_added_at: Optional[datetime]


async def get_groups(domain: str, api_key: str) -> list[GCGroup]:
    url = f'{GC_API_URL}/groups'.format(domain=domain)
    params = {'key': api_key}
    async with ClientSession() as session:
        async with session.get(url, params=params) as response:
            data = await response.json()
            if not data['success'] or data['error']:
                exception = resolve_error(
                    data['error_code'],
                    data['error_message']
                )
                raise exception

            return [GCGroup(**group) for group in data['info']]


def resolve_error(
    error_code: int,
    error_message: str,
) -> GetCourseApiException:
    if error_code == 901:
        return UnauthorizedRequest(error_message)
    elif error_code == 904:
        return KeyNotSpecified(error_message)
    elif error_code == 908:
        return FiltersRequired(error_message)
    elif error_code == 912:
        return IncorrectDate(error_message)
    elif error_code == 914:
        return IncorrectStatus(error_message)
    else:
        return UnknownException(error_message)
