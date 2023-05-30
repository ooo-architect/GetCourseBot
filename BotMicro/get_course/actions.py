from typing import Optional

from odetam.query import DetaQueryList

from get_course.utils.api import get_groups
from models.account import Account
from models.group import Group
from models.member import Member


async def create_account(domain: str) -> Optional[Account]:
    account = await Account.get_or_none(domain)
    if account is not None:
        return account

    account = Account(key=domain, domain=domain)  # type: ignore
    await account.save()  # type: ignore
    return account


async def update_account_groups(
    account_key: str,
    api_key: str,
) -> Optional[list[Group]]:
    account = await Account.get_or_none(account_key)
    if account is None:
        return None

    groups = await get_groups(account_key, api_key)

    existed_groups = await Group.query(
        DetaQueryList([
            Group.gid == group.id
            for group in groups
        ])  # type: ignore
    )
    existed_gids = [group.gid for group in existed_groups]
    new_groups = [
        Group(key=group.id, gid=group.id, name=group.name)
        for group in groups if group.id not in existed_gids
    ]
    all_groups = existed_groups + new_groups

    created_groups: list[Group] = await Group.put_many(all_groups)
    account.groups = [group.key for group in created_groups]
    await account.save()  # type: ignore
    return created_groups


async def register_group_member(
    gid: str,
    uid: str,
    user_id: int
) -> Optional[Member]:
    member = await Member.get_or_none(uid)
    if member is None:
        return None

    member.user_id = user_id
    await member.save()

    group = await Group.get_or_none(gid)
    if group is None:
        return None

    if member.uid not in group.unchecked_members:
        group.unchecked_members.append(member.uid)

    await group.save()
    return member
