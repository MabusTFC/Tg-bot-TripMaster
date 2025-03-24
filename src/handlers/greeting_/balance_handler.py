from aiogram import (
    Router,
    types,
)
from aiogram.types import CallbackQuery


from handlers.utils.answer import BALANCE_MESSAGE
from handlers.utils.keyboards import get_balance_keyboard

router = Router()

@router.callback_query(lambda c: c.data == "balance")
async def balance_handler(callback_query: CallbackQuery):
    await callback_query.message.answer_photo(
        caption=BALANCE_MESSAGE,
        parse_mode="Markdown",
        photo=types.FSInputFile("img/balance.png"),
        reply_markup=await get_balance_keyboard()
    )
    await callback_query.answer()