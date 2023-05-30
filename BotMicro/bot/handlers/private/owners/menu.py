from aiogram import Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot import messages
from bot.callbacks.owner import AccountMenuCallback
from bot.keyboards.owner import account_menu_kb
from bot.utils.api_key import get_api_key
from get_course.actions import update_account_groups
from models.account import Account
from utils.logging import log_to_deta

router = Router()


@router.callback_query(AccountMenuCallback.filter())
async def open_account_menu_handler(query: CallbackQuery, callback_data: AccountMenuCallback, bot: Bot, state: FSMContext):
    await query.answer()
    await state.clear()

    message = query.message
    if not message:
        return

    account = await Account.get_or_none(callback_data.account)
    if account is None:
        return await message.answer(messages.ERROR)

    api_key = await get_api_key(message.chat.id, bot)
    if api_key is None:
        return await message.answer(messages.API_KEY_NOT_FOUND)

    groups = await update_account_groups(account.key, api_key)
    if groups is None:
        await log_to_deta({
            'account': account.key,
            'api_key': api_key,
            'groups': groups,
        })
        return await message.answer(messages.ERROR)

    await message.edit_text(
        messages.ACCOUNT_MENU,
        reply_markup=account_menu_kb(account.key, groups)
    )
