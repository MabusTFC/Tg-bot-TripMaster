from aiogram import Router, types
from aiogram.types import CallbackQuery


from handlers.utils.answer import MANUAL_MESSAGE
from handlers.utils.keyboards import get_support_keyboard

router = Router()

@router.callback_query(lambda c: c.data == "manual")
async def manual_handler(callback_query: CallbackQuery):
    await callback_query.message.answer_photo(
        caption=MANUAL_MESSAGE,
        parse_mode="Markdown",
        reply_markup=await get_support_keyboard(),
        photo=types.FSInputFile("img/manual.jpeg"),

    )
    await callback_query.answer()