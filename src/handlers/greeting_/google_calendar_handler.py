from aiogram import (
    Router,
    types,
)
from aiogram.types import CallbackQuery


from handlers.utils.answer import MANUAL_MESSAGE
from handlers.utils.keyboards import get_google_calendar_keyboard

router = Router()

@router.callback_query(lambda c: c.data == "g_calendar")
async def balance_handler(callback_query: CallbackQuery):
    await callback_query.message.answer_photo(
        caption=MANUAL_MESSAGE,
        parse_mode="Markdown",
        photo=types.FSInputFile("img/zaglushka.jpg"),
        reply_markup=await get_google_calendar_keyboard()
    )
    await callback_query.answer()