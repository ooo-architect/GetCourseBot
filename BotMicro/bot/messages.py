from typing import Optional

from aiogram.types import ChatInviteLink

from models.group import Group
from models.member import Member

WRONG_START_LINK = 'Неправильная ссылка. Обратитесь к администратору курса.'

MEMBER_ACCESS_ERROR = 'Вы не состоите в этой группе.'

ERROR = 'Произошла ошибка, попробуйте позже'
CANCEL = 'Действие отменено'

OWNER_GREETING = '''
Кнопка ниже только для администраторов. Если Вы участник курсов и Вам не пришли ссылки, обратитесь к админам
'''

ASK_DOMAIN = 'Укажите хост вашего аккаунта GetCourse. Вы можете скопировать его из интернет-адреса вашего личного кабинета. Он будет иметь вид ИМЯ_АККАУНТА.getcourse.ru или просто ваш домен, если вы подключили собственный домен к GetCourse:'
INCORRECT_DOMAIN = 'Некорректный домен. Домен должен быть длиной не более 35 символов и содержать только английские буквы, цифры тире и точки. Попробуйте снова:'
ASK_API_KEY = 'Укажите ключ доступа к GetCourse. Вы можете получить его по адресу https://{domain}/saas/account/api'
API_KEY_MESSAGE_WARNING = 'Пожалуйста, не изменяйте и не открепляйте сообщение с ключом доступа. Это позволяет нам не хранить ваши секретные данные на сервере.'
SUCCESS_ACCOUNT_CREATION = '✅ Аккаунт успешно подключен.'
ERROR_ACCOUNT_CREATION = 'Произошла ошибка. Попробуйте позже.'

API_KEY_NOT_FOUND = 'Не найден ключ доступа. Попробуйте снова привязать аккаунт: /start'

ACCOUNT_MENU = 'Управление курсами'
GROUP_MENU = 'Управление {name}.\nНажмите на чат в списке, чтобы удалить.'

CHAT_CONNECT_INSTRUCTION = 'Добавьте бота в группу, сделайте администратором и введите эту команду:\n<code>/connect {account} {group}</code>'
SUCCESS_CONNECT_CHAT = '✅ Чат подключен'

INCORRECT_MESSAGE_TYPE = 'Неверный тип сообщения. Попробуйте снова'

EDIT_INVITE_TEXT_INSTRUCTION = '''
Введите текст, который будет отображаться в приглашении участников.
{member.name} заменится на имя участника,
а {invite_links} - на ссылки на подключенные чаты:
'''
SUCCESS_EDIT_INVITE_TEXT = '✅ Текст успешно обновлен'

EDIT_INVITE_IMAGE_INSTRUCTION = '''
Пришлите изображение, которое будет отображаться в приглашении участников.
Отправьте /empty, чтобы сбросить
'''
SUCCESS_EDIT_INVITE_IMAGE = '✅ Изображение успешно обновлено'
SUCCESS_REMOVE_INVITE_IMAGE = '✅ Изображение успешно убрано'


def group_menu_header(group: Group, start_link: str, add_link: str, remove_link: str) -> str:
    return f'''
Управление {group.name}

Ссылка для доступа к чатам:
{start_link}

Ссылка для процесса добавления участника:
{add_link}


Ссылка для процесса удаления участника:
{remove_link}

Нажмите на чат, чтобы открепить его или на кнопку "➕ Добавить чат", чтобы добавить новый.
Не забудьте добавить бота в администраторы чатов.
'''


DEFAULT_INVITE_TEXT = '''
Вам доступны закрытые чаты курса:

{invite_links}
'''


def invite_message(invite_text: Optional[str], member: Member, invite_links: list[ChatInviteLink]) -> str:
    if not invite_text:
        invite_text = DEFAULT_INVITE_TEXT

    links_block = ''
    for link in invite_links:
        links_block += f'<b>{link.name}</b>\n➡️{link.invite_link}\n'

    try:
        text = invite_text.format(invite_links=links_block, member=member)
    except:
        text = DEFAULT_INVITE_TEXT.format(invite_links=links_block)

    return text
