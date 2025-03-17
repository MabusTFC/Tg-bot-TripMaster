from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
import logging

from handlers.utils.keyboards import (
    get_days_keyboard,
    get_list_sity_keyboard,
)


router = Router()

@router.callback_query(lambda c: c.data.startswith("select_"))
async def select_city(callback_query: CallbackQuery, state: FSMContext):
    city_index = int(callback_query.data.split("_")[1])
    user_data = await state.get_data()
    route = user_data.get("route", [])
    user_days = user_data.get("user_days", {})

    if city_index >= len(route):
        await callback_query.answer("Ошибка! Город не найден.")
        return

    city = route[city_index]
    days = user_days.get(city, 1)

    await state.update_data(selected_city=city)
    await callback_query.message.edit_text(
        f"Вы выбрали город: {city}\nВыберите количество дней пребывания:",
        reply_markup=await get_days_keyboard(city, days)
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data.startswith("increase_") or c.data.startswith("decrease_"))
async def change_days(callback_query: CallbackQuery, state: FSMContext):
    action, city = callback_query.data.split("_")
    user_data = await state.get_data()
    user_days = user_data.get("user_days", {})

    current_days = user_days.get(city, 1)

    if action == "increase":
        current_days += 1
    elif action == "decrease" and current_days > 1:
        current_days -= 1

    user_days[city] = current_days
    await state.update_data(user_days=user_days)

    await callback_query.message.edit_reply_markup(reply_markup=await get_days_keyboard(city, current_days))
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