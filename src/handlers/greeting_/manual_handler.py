from aiogram import Router, types
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from handlers.utils.answer import MANUAL_MESSAGE
from handlers.utils.keyboards import get_support_keyboard, get_greetings_keyboard

router = Router()


@router.callback_query(lambda c: c.data == "manual")
async def manual_handler(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer_photo(
        caption=MANUAL_MESSAGE,
        parse_mode="Markdown",
        reply_markup=await get_support_keyboard(),
        photo=types.FSInputFile("img/logoTrip.png"),
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "back_to_menu")
async def back_to_menu_handler(callback_query: CallbackQuery, state: FSMContext):
    # Получаем данные пользователя из состояния
    data = await state.get_data()
    tg_id = data.get('tg_id')
    user_name = callback_query.from_user.first_name

    # Получаем баланс пользователя (предполагая, что у вас есть такая функция)
    from database.database_manager import get_user_balance
    balance = await get_user_balance(tg_id)

    # Отправляем сообщение с главным меню
    await callback_query.message.answer_photo(
        photo=types.FSInputFile("img/logoTrip.png"),
        caption=f"Добро пожаловать, {user_name}! Ваш баланс: {balance} токенов.",
        parse_mode="Markdown",
        reply_markup=await get_greetings_keyboard(),
    )
    await callback_query.answer()