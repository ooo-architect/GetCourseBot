from aiogram import Bot
from fastapi import APIRouter, Depends, HTTPException, status

from bot.utils.groups import kick_members_in_many_chats
from models.group import Group
from models.member import Member
from utils.logging import log_to_deta
from web.stubs import BotStub

members_router = APIRouter(prefix='/members', tags=['GetCourse'])


@members_router.get('/add')
async def add_member(
    domain: str,
    gid: str,
    uid: str,
    name: str,
) -> bool:
    await log_to_deta({
        'event': 'add_member',
        'data': {
            'domain': domain,
            'gid': gid,
            'uid': uid,
            'name': name,
        }
    })
    group = await Group.get_or_none(gid)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Group not found'
        )

    if uid not in group.unchecked_members:
        group.unchecked_members.append(uid)

    await group.save()

    member = await Member.get_or_none(uid)
    if not member:
        member = Member(key=uid, uid=uid, name=name)
        await member.save()

    return True


@members_router.get('/remove')
async def remove_member(
    domain: str,
    gid: str,
    uid: str,
    bot: Bot = Depends(BotStub),
) -> bool:
    await log_to_deta({
        'event': 'remove_member',
        'data': {
            'domain': domain,
            'gid': gid,
            'uid': uid,
        }
    })
    group = await Group.get_or_none(gid)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Group not found')

    if uid in group.unchecked_members:
        group.unchecked_members.remove(uid)

    await group.save()

    member = await Member.get_or_none(uid)
    if not member:
        return False

    kicked_members = await kick_members_in_many_chats(
        [member.user_id],
        group.connected_chats,
        bot
    )
    return bool(kicked_members)
