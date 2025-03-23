
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from handlers.utils.keyboards import (
    get_number_keyboard,
    get_days_keyboard,
)

router = Router()

@router.callback_query(lambda c: c.data.startswith("choose_city_"))
async def choose_days_handler(callback_query: CallbackQuery, state: FSMContext):
    print(f"DEBUG: callback_data = {callback_query.data}")

    _, city = callback_query.data.split("_", 1)  # Разбираем callback_data
    user_data = await state.get_data()

    total_days = user_data.get("total_days", 30)
    max_days = user_data.get("max_days", total_days)
    user_days = user_data.get("user_days", {})

    await callback_query.message.edit_text(
        "Выберите количество дней:",
        reply_markup=await get_number_keyboard(city, user_days.get(city, 1), max_days)
    )


@router.callback_query(lambda c: c.data.startswith("choose_number_"))
async def set_days(callback_query: CallbackQuery, state: FSMContext):

    print(f"DEBUG: callback_data = {callback_query.data}")

    data = callback_query.data.split("_")

    if len(data) != 3:
        await callback_query.answer(f"Ошибка! Неверный формат данных: {callback_query.data}")
        return

    _, city, days = data
    days = int(days)

    user_data = await state.get_data()
    total_days = user_data.get("total_days", 30)
    max_days = user_data.get("max_days", total_days)
    user_days = user_data.get("user_days", {})

    user_days[city] = days
    max_days = total_days - sum(user_days.values())  # Пересчитываем оставшиеся дни

    await state.update_data(user_days=user_days, max_days=max_days)

    await callback_query.message.edit_text(
        f"Вы выбрали {days} дн для {city}:",
        reply_markup=await get_days_keyboard(city, days, max_days)
    )