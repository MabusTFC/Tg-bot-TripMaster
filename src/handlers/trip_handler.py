from aiogram import Router, types
from aiogram.fsm import state
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery


from handlers.utils.state_machine import DateSelection

router = Router()

@router.callback_query(lambda c: c.data == "create_trip")
async def trip_handler(callback_query: CallbackQuery):
    await callback_query.message.answer("Введите начальный город")
    await state.set_state(DateSelection.START_DATE)
    await callback_query.answer()

@router.message()
async def process_city_input(message: types.Message, state: FSMContext):
    user_data = await state.get_data()

    if "point_a" not in user_data:
        await state.update_data(point_a=message.text)
        await message.answer(f"Начальный город: {message.text} \nТеперь введите конечный город ")

    else:
        point_a = user_data["point_a"]
        point_b = message.text

        await message.answer(f"Маршрут сохранен!\n\n Старт: {point_a}\nФиниш: {point_b}")
        await state.clear()