from aiogram import Router, types
from aiogram.types import CallbackQuery

from handlers.utils.answer import SUPPORT_TEH_MESS

router = Router()

@router.callback_query(lambda c: c.data == "support")
async def support_handler(callback_query: CallbackQuery):
    await callback_query.message.answer_photo(
        caption=SUPPORT_TEH_MESS,
        parse_mode="MarkdownV2",
        photo=types.FSInputFile("img/SupportPhoto.png")
    )
    await callback_query.answer()