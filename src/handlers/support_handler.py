from aiogram import Router, types
from aiogram.types import CallbackQuery



router = Router()

@router.callback_query(lambda c: c.data == "support")
async def support_handler(callback_query: CallbackQuery):
    await callback_query.message.answer_photo(
        caption="Тех.подержка",
        parse_mode="Markdown",
        photo=types.FSInputFile("img/zaglushka.jpg")
    )
    await callback_query.answer()