from aiogram import Bot, Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, Message

from bot import messages
from bot.utils.deeplinks import decode_link_args
from bot.utils.groups import get_personal_invite_links
from get_course.actions import register_group_member
from models.group import Group
from models.member import Member

router = Router()


@router.message(CommandStart(deep_link=True))
async def start_handler(message: Message, command: CommandObject, bot: Bot, state: FSMContext):
    await state.clear()

    if not message.from_user or not command.args:
        return await message.answer(messages.WRONG_START_LINK)

    args = decode_link_args(command.args)
    if not args or len(args) != 3:
        await message.answer(messages.WRONG_START_LINK)
        return {'args': args}

    domain, gid, uid = args

    group = await Group.get_or_none(gid)
    if group is None:
        return await message.answer(messages.WRONG_START_LINK)

    member = await Member.get_or_none(uid)
    if member is None:
        await message.answer(messages.MEMBER_ACCESS_ERROR)
        members = await Member.get_all()
        return {'domain': domain, 'uid': uid, 'gid': gid, 'members': [member.key for member in members]}

    if uid not in group.unchecked_members:
        await message.answer(messages.MEMBER_ACCESS_ERROR)
        return {'domain': domain, 'uid': uid, 'gid': gid, 'members': group.unchecked_members}

    await register_group_member(gid=gid, uid=uid, user_id=message.from_user.id)

    invite_links = await get_personal_invite_links(group.connected_chats, bot)
    invite_image_file = group.get_invite_image()
    invite_text = messages.invite_message(
        group.invite_text, member, invite_links)
    if invite_image_file:
        invite_image = BufferedInputFile(
            invite_image_file.read(), 'invite_img.png')
        await message.answer_photo(
            photo=invite_image,
            caption=invite_text
        )
    else:
        await message.answer(invite_text)
