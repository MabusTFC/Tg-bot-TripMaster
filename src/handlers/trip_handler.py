from aiogram import Router, types
from aiogram.fsm import state
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.utils.state_machine import (
    DateSelection,
    RoutStates,
)

from handlers.utils.keyboards import (
    get_selection_keyboard,
    get_calendar_keyboard
)

router = Router()

@router.callback_query(lambda c: c.data == "create_trip")
async def trip_handler(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(route=[])
    await callback_query.message.answer("Введите начальный город:")
    await state.set_state(RoutStates.SELECT_CITY)
    await callback_query.answer()

@router.message(RoutStates.SELECT_CITY)
async def process_city_input(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    route = user_data.get("route", [])

    route.append(message.text)
    await state.update_data(route=route)

    if len(route) == 1:
        await message.answer(f"Начальный город: {message.text} \nТеперь введите конечный город.")
    else:
        await message.answer(f"Маршрут сохранен!\nГорода маршрута: {' → '.join(route)}",
                             reply_markup=await get_calendar_keyboard()
                             )
        await state.set_state(DateSelection.START_DATE)
