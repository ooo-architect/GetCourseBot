from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot import messages
from bot.keyboards.owner import start_account_connection_kb

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(
        messages.OWNER_GREETING,
        reply_markup=start_account_connection_kb()
    )
