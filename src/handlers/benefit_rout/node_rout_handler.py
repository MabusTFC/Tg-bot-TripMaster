from aiogram import Router, types

from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


from handlers.utils.state_machine import RoutStates
from handlers.utils.keyboards import get_zveno_rout_keyboard

router = Router()

@router.callback_query(lambda c: c.data == "benefit_rout")
async def node_rout_handler(callback_query: CallbackQuery,state: FSMContext):
    await state.set_state(RoutStates.ZVENO_ROUT)
    await callback_query.message.answer(text="Введите список городов через запятую:")


@router.message(RoutStates.ZVENO_ROUT)
async def node_input_cities(message: types.Message, state: FSMContext):
    global temp_cities
    user_data = await state.get_data()
    total_days = user_data.get("total_days", 30)
    max_days = user_data.get("max_days",total_days)
    current_days = user_data.get("current_days_zveno", 1)

    temp_cities = [city.strip() for city in message.text.split(",") if city.strip()]
    await state.update_data(temp_cities=temp_cities, current_days_zveno=current_days)


    await message.answer("Настройте количество дней:", reply_markup=await get_zveno_rout_keyboard(current_days,max_days))


@router.callback_query(lambda c: c.data.startswith("pluse_days") or c.data.startswith("minus_days"))
async def change_days_count(callback_query: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    total_days = user_data.get("total_days", 30)
    max_days = user_data.get("max_days", total_days)
    current_days = user_data.get("current_days_zveno", 1)

    action = callback_query.data

    if action == "pluse_days" and current_days < max_days:
        current_days += 1
        max_days -= 1

    elif action == "minus_days" and current_days > 1:
        current_days -= 1
        max_days += 1

    await state.update_data(current_days=current_days, max_days=max_days)

    print(f"DEBUG: Action: {action}, max_days: {max_days}, current_days_zveno: {current_days}")

    new_markup = await get_zveno_rout_keyboard(current_days, max_days)

    if callback_query.message.reply_markup != new_markup:
        await callback_query.message.edit_reply_markup(reply_markup=new_markup)

    await callback_query.answer()


@router.callback_query(lambda c: c.data == "add_zveno")
async def add_node(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(RoutStates.ZVENO_ROUT)
    await callback_query.message.answer("Введите список городов для нового звена:")

    user_data = await state.get_data()
    temp_cities = user_data.get("temp_cities", [])
    days_count = user_data.get("current_days_zveno", 1)
    zveno_list = user_data.get("zveno_list", [])

    if temp_cities:
        new_zveno ={city: days_count for city in temp_cities}
        zveno_list.append(new_zveno)

        await state.update_data(zveno_list=zveno_list, temp_cities=[], current_days_zveno=1)


@router.callback_query(lambda c: c.data == "save_zveno")
async def save_node(callback_query: CallbackQuery,state: FSMContext):
    user_data = await state.get_data()
    temp_cities = user_data.get("temp_cities", [])
    days_count = user_data.get("current_days_zveno", 1)
    zveno_list = user_data.get("zveno_list", [])

    if temp_cities:
        new_zveno = {city: days_count for city in temp_cities}
        zveno_list.append(new_zveno)

        await state.update_data(zveno_list=zveno_list, temp_cities=[], current_days_zveno=1)

    formatted_zveno_list = "\n".join(
        [f"{i + 1} звено: {dict(zveno)}" for i, zveno in enumerate(zveno_list)]
    )
    print(formatted_zveno_list)

    await callback_query.message.answer(f"Звено сохранено!\nТекущие звенья: {zveno_list}")


