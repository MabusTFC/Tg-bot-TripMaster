from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from handlers.utils.answer import GUIDE_MESSAGE

router = Router()


@router.callback_query(lambda c: c.data == "guide")
async def authorization_google(callback_query: CallbackQuery, state: FSMContext):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="manual")]
    ])

    await callback_query.message.answer_photo(
        caption=GUIDE_MESSAGE,
        parse_mode="Markdown",
        photo=types.FSInputFile("img/manual.jpeg"),
        reply_markup=keyboard
    )
    await callback_query.answer()