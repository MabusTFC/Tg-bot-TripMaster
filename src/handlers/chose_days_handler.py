
from aiogram import (
    Router,
    types,
)
from aiogram.fsm import state
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery


from handlers.utils.keyboards import (
    get_number_keyboard,
    get_days_keyboard,
)

router = Router()


async def choose_days(callback_query: CallbackQuery):
    city = callback_query.data.split('_')[2]
    user_data = await state.get_data()
    total_days = user_data.get("total_days", 30)
    max_days = user_data.get("max_days", total_days)
    user_days = user_data.get("user_days", {})

    keyboard = await get_number_keyboard(city, user_days, max_days)
    await callback_query.message.edit_text("Выберите количество дней:", reply_markup=keyboard)



async def set_days(callback_query: CallbackQuery):
    action, city = callback_query.data.split("_")
    user_data = await state.get_data()
    total_days = user_data.get("total_days", 30)
    max_days = user_data.get("max_days", total_days)
    user_days = user_data.get("user_days", {})

    current_days = user_days.get(city, 1)

    max_days = max_days - current_days

    user_days[city] = current_days
    await state.update_data(user_days=user_days, max_days=max_days)


    keyboard = await get_days_keyboard(city, user_days)
    await callback_query.message.edit_text(f"Вы выбрали {current_days} дн:", reply_markup=keyboard)