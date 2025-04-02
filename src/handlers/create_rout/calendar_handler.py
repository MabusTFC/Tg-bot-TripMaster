import datetime

from aiogram import Router, types
from aiogram.fsm import state
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.utils.state_machine import (
    RoutStates,
    DateSelection
)
from handlers.utils.keyboards import (
    get_selection_keyboard,
    get_calendar_keyboard,
)

router = Router()



@router.callback_query(lambda c: c.data.startswith("change_month-"))
async def change_month(callback_query: CallbackQuery):
    _, year, month = callback_query.data.split("-")
    year, month = int(year), int(month)


    await callback_query.message.edit_reply_markup(reply_markup=await get_calendar_keyboard(year, month))
    await callback_query.answer()



@router.callback_query(lambda c: c.data.startswith("date_"))
async def process_start_date(callback_query: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()

    if current_state == DateSelection.END_DATE:
        await process_end_date(callback_query, state)
        return


    selected_date = callback_query.data.split("_")[1]
    selected_date_obj = datetime.datetime.strptime(selected_date, "%Y-%m-%d")
    today = datetime.datetime.now().date()

    if selected_date_obj.date() < today:
        await callback_query.answer("❌ Нельзя выбрать прошедшую дату!")
        return

    await state.update_data(start_date=selected_date)

    await callback_query.message.edit_text(
        f"📆 Дата отправления выбрана: {selected_date}\nТеперь выберите дату возвращения.",
        reply_markup=await get_calendar_keyboard()
    )
    await state.set_state(DateSelection.END_DATE)
    await callback_query.answer()



@router.callback_query(lambda c: c.data.startswith("date_"), DateSelection.END_DATE)
async def process_end_date(callback_query: CallbackQuery, state: FSMContext):
    selected_date = callback_query.data.split("_")[1]
    user_data = await state.get_data()

    start_date = user_data.get("start_date")

    start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = datetime.datetime.strptime(selected_date, "%Y-%m-%d")

    if datetime.datetime.strptime(selected_date, "%Y-%m-%d") < datetime.datetime.strptime(start_date, "%Y-%m-%d"):
        await callback_query.answer("❌ Дата возвращения не может быть раньше даты отправления!")
        return

    total_days = (end_date_obj - start_date_obj).days


    await state.update_data(end_date=selected_date, total_days=total_days)

    await callback_query.message.edit_text(
        f"✅ Выбранный маршрут:\n"
        f"📍 Города: {' → '.join(user_data.get('route', []))}\n"
        f"📆 Дата отправления: {start_date}\n"
        f"📆 Дата возвращения: {selected_date}\n\n"
        f"⏳ Длительность поездки: {total_days} дней\n\n"
        f"Выберите следующий шаг:",
        reply_markup=await get_selection_keyboard()
    )

    await callback_query.answer()
