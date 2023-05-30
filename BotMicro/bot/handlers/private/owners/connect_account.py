from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot import messages
from bot.callbacks.owner import AccountConnectionCallback
from bot.keyboards.owner import open_account_menu_kb
from bot.states.owner import AccountConnectionState
from bot.utils.deeplinks import validate_domain
from get_course.actions import create_account
from utils.logging import log_to_deta

router = Router()


@router.callback_query(AccountConnectionCallback.filter())
async def account_connection_handler(query: CallbackQuery, state: FSMContext):
    await query.answer()
    await state.clear()

    message = query.message
    if not message:
        return

    await message.answer(messages.ASK_DOMAIN)
    await state.set_state(AccountConnectionState.domain)


@router.message(AccountConnectionState.domain, F.text)
async def domain_handler(message: Message, state: FSMContext):
    if not message.text:
        return

    try:
        domain = validate_domain(message.text)
    except ValueError:
        return await message.answer(messages.INCORRECT_DOMAIN)

    await message.answer(messages.ASK_API_KEY.format(domain=domain))

    await state.update_data(domain=domain)
    await state.set_state(AccountConnectionState.api_key)


@router.message(AccountConnectionState.api_key, F.text, F.text.as_('text'))
async def api_key_handler(message: Message, text: str, state: FSMContext):
    if not message.text:
        return

    data = await state.get_data()
    domain = data.get('domain')
    if domain is None:
        return

    account = await create_account(domain=domain)
    if account is None:
        await message.answer(messages.ERROR_ACCOUNT_CREATION)
        return

    await message.pin(disable_notification=True)
    await message.answer(messages.API_KEY_MESSAGE_WARNING)
    await message.answer(
        messages.SUCCESS_ACCOUNT_CREATION,
        reply_markup=open_account_menu_kb(account.key)
    )

    await state.clear()
