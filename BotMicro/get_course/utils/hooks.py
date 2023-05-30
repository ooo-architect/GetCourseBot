from os import getenv
from typing import Optional

host = getenv('DETA_SPACE_APP_HOSTNAME', '')
HOOKS_URL = 'https://' + host + '/members'


def get_hook_add_link(
    domain: str,
    gid: str,
    uid: Optional[str] = None,
    name: Optional[str] = None,
) -> str:
    uid_stub = uid or '{object.id}'
    name_stub = name or '{object.name}'
    link = '/add?domain={domain}&gid={gid}&uid={uid_stub}&name={name_stub}'.format(
        domain=domain,
        gid=gid,
        uid_stub=uid_stub,
        name_stub=name_stub,
    )
    return HOOKS_URL + link


def get_hook_remove_link(
    domain: str,
    gid: str,
) -> str:
    uid_stub = '{object.id}'
    link = '/remove?domain={domain}&gid={gid}&uid={uid_stub}'.format(
        domain=domain,
        gid=gid,
        uid_stub=uid_stub,
    )
    return HOOKS_URL + link
