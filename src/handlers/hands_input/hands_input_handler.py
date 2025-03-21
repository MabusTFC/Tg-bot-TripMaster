from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.utils.keyboards import (
    get_selection_keyboard,
    get_list_sity_keyboard,
    get_days_keyboard,
)

from handlers.utils.state_machine import RoutStates


router = Router()

@router.callback_query(lambda c: c.data == "hands_input")
async def hands_input_handler(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Введите промежуточные города через запятую: ")
    await state.set_state(RoutStates.ADD_CITY)
    await callback_query.answer()


@router.message(RoutStates.ADD_CITY)
async def process_intermediate_cities(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    route = user_data.get("route", [])
    user_days = user_data.get("user_days", {})

    new_cities = [city.strip() for city in message.text.split(",") if city.strip()]

    if len(route) >= 2:
        route = [route[0]] + new_cities + [route[-1]]
    else:
        route.extend(new_cities)

    await state.update_data(route=route, user_days=user_days)

    await message.answer(f"Маршрут дополнен!\nГорода маршрута: {' → '.join(route)}",
                         reply_markup=await get_list_sity_keyboard(route, user_days)
                         )


@router.callback_query(lambda c: c.data.startswith("page_"))
async def change_page(callback_query: CallbackQuery, state: FSMContext):
    page = int(callback_query.data.split("_")[1])
    user_data = await state.get_data()
    route = user_data.get("route", [])
    user_days = user_data.get("user_days", {})

    await callback_query.message.edit_reply_markup(reply_markup=await get_list_sity_keyboard(route, user_days, page))
    await callback_query.answer()


