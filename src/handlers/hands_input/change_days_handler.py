
from aiogram import (
    Router,
    types,
)
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery


from handlers.utils.keyboards import (
    get_days_keyboard,
    get_list_sity_keyboard
)

from handlers.utils.state_machine import DateSelection

router = Router()


@router.callback_query(lambda c: c.data.startswith("increase_") or c.data.startswith("decrease_"))
async def change_days(callback_query: CallbackQuery, state: FSMContext):
    action, city = callback_query.data.split("_")
    user_data = await state.get_data()
    total_days = user_data.get("total_days", 30)
    max_days = user_data.get("max_days", total_days)
    user_days = user_data.get("user_days", {})

    current_days = user_days.get(city, 1)

    if action == "increase" and current_days < max_days:
        current_days += 1
        max_days-=1

    elif action == "decrease" and current_days > 1:
        current_days -= 1
        max_days+=1

    user_days[city] = current_days
    await state.update_data(user_days=user_days, max_days=max_days)

    print(
        f"DEBUG: City: {city}, Action: {action}, max_days: {max_days}, current_days: {current_days}, user_days: {user_days}"
    )

    await callback_query.message.edit_reply_markup(reply_markup=await get_days_keyboard(city, current_days, max_days))
    await callback_query.answer()



@router.callback_query(lambda c: c.data == "back_to_cities")
async def back_to_cities(callback_query: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    route = user_data.get("route", [])
    user_days = user_data.get("user_days", {})

    await callback_query.message.edit_text(
        "Выберите город из списка:",
        reply_markup=await get_list_sity_keyboard(route, user_days)
    )
    await callback_query.answer()