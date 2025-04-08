from aiogram import Router, types
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from handlers.utils.answer import SUPPORT_TEH_MESS

router = Router()


@router.callback_query(lambda c: c.data == "support")
async def support_handler(callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="manual")]
    ])

    await callback_query.message.answer_photo(
        caption=SUPPORT_TEH_MESS,
        parse_mode="MarkdownV2",
        photo=types.FSInputFile("img/SupportPhoto.png"),
        reply_markup=keyboard
    )
    await callback_query.answer()