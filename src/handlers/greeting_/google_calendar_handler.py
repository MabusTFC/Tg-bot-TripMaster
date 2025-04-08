from aiogram import (
    Router,
    types,
)
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.filters import Command

from handlers.utils.answer import MANUAL_MESSAGE
from handlers.utils.keyboards import (
    get_google_calendar_keyboard,
    get_greetings_keyboard
)
from database.database_manager import get_user_balance

router = Router()


@router.callback_query(lambda c: c.data == "g_calendar")
async def calendar_handler(callback_query: CallbackQuery):
    await callback_query.message.answer_photo(
        caption=MANUAL_MESSAGE,
        parse_mode="Markdown",
        photo=types.FSInputFile("img/calendar.jpg"),
        reply_markup=await get_google_calendar_keyboard()
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "back_to_menu_from_calendar")
async def back_to_menu_from_calendar_handler(callback_query: CallbackQuery, state: FSMContext):
    # Получаем данные пользователя
    tg_id = callback_query.from_user.id
    user_name = callback_query.from_user.first_name

    # Получаем текущий баланс
    balance = await get_user_balance(tg_id)

    # Отправляем сообщение с главным меню
    await callback_query.message.answer_photo(
        photo=types.FSInputFile("img/logoTrip.png"),
        caption=f"Добро пожаловать, {user_name}! Ваш баланс: {balance} токенов.",
        parse_mode="Markdown",
        reply_markup=await get_greetings_keyboard(),
    )
    await callback_query.answer()