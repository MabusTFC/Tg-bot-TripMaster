from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
import logging

from handlers.utils.keyboards import (
    get_days_keyboard,
    get_list_sity_keyboard,
)

from handlers.utils.state_machine import RoutStates

router = Router()

@router.callback_query(lambda c: c.data.startswith("select_"))
async def select_city(callback_query: CallbackQuery, state: FSMContext):
    city_index = int(callback_query.data.split("_")[1])
    user_data = await state.get_data()
    total_days = user_data.get("total_days")
    max_days = user_data.get("max_days", total_days)
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
        reply_markup=await get_days_keyboard(city, days, max_days)
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "finish_selection")
async def finish_selection(callback_query: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    route = user_data.get("route", [])
    user_days = user_data.get("user_days", {})


    final_selection = [(city, user_days.get(city, 1)) for city in route]

    await state.update_data(final_selection=final_selection)
    await state.set_state(RoutStates.FINAL_ROUTE)

    await callback_query.message.edit_text("Маршрут сохранен! Вы можете перейти к следующему шагу.")
    await callback_query.answer()