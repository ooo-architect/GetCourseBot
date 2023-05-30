from os import getenv
from string import ascii_lowercase, digits

DOMAIN_SYMBOLS = ascii_lowercase + digits + '.-'


def validate_domain(domain: str) -> str:
    domain = domain.lower()
    if len(domain.replace('getcourse', '')) > 35:
        raise ValueError('Domain must be shorter then 35 characters')

    if any([symbol not in DOMAIN_SYMBOLS for symbol in domain]):
        raise ValueError('Domain contains incorrect symbols')

    return domain


DOT = 'D'
DELIMITER = '_'
GET_COURSE = 'GC'


def decode_link_args(args_str: str) -> list[str]:
    args_str = args_str.replace(DOT, '.')
    args_str = args_str.replace(GET_COURSE, 'getcourse')
    args = args_str.split(DELIMITER)
    return args


def encode_link_args(*args: str) -> str:
    args_str = DELIMITER.join(args)
    args_str = args_str.replace('.', DOT)
    args_str = args_str.replace('getcourse', GET_COURSE)
    return args_str


def get_private_deeplink(*args: str) -> str:
    base_link = getenv('BOT_LINK')

    args_str = encode_link_args(*args)
    link = f'{base_link}?start={args_str}'
    return link


def get_group_deeplink(*args: str) -> str:
    base_link = getenv('BOT_LINK')

    args_str = encode_link_args(*args)
    link = f'{base_link}?startgroup={args_str}'
    return link
