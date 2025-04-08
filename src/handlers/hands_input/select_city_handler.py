import datetime
import requests
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,

)

from Algorithm.FindCheapestWay import get_routes


from handlers.utils.keyboards import (
    get_days_keyboard,
    get_list_sity_keyboard,
)

from handlers.utils.state_machine import RoutStates

from database.database_manager import *

router = Router()

@router.callback_query(lambda c: c.data.startswith("select_"))
async def select_city(callback_query: CallbackQuery, state: FSMContext):
    city_index = int(callback_query.data.split("_")[1])
    user_data = await state.get_data()
    total_days = user_data.get("total_days")
    max_days = user_data.get("max_days", total_days)
    route = user_data.get("route", [])
    user_days = user_data.get("user_days", [])
    user_days_dict = dict(user_days)

    if city_index >= len(route):
        await callback_query.answer("Ошибка! Город не найден.")
        return

    city = route[city_index]
    days = user_days_dict.get(city, 1)

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
    start_date = user_data.get("start_date")
    user_days = user_data.get("user_days", {})

    tg_id = callback_query.from_user.id

    # Получаем маршруты
    start_city = route[0]
    end_city = route[-1]  # Берем последний город как конечный
    departure_date = start_date
    segments = list(user_days.items())

    routes = get_routes(start_city, end_city, departure_date, segments)

    # Сохраняем маршруты в базу данных
    try:
        # Сохраняем каждый маршрут отдельно
        for route_data in routes:
            await save_route_with_details(
                tg_id=tg_id,
                cities=route_data["route"],
                route_details=route_data
            )
    except Exception as e:
        print(f"Ошибка при сохранении маршрута: {e}")
        await callback_query.message.answer("Ошибка при сохранении маршрутов. Попробуйте позже.")
        return

    # Отправка маршрутов на сервер (если это все еще нужно)
    try:
        server_url = "https://5d66-57-129-20-222.ngrok-free.app/api/save-routes"
        response = requests.post(server_url, json={"user_id": str(tg_id), "routes": routes})

        if response.status_code != 200:
            print(f"Ошибка при отправке маршрутов на сервер: {response.status_code}")
    except Exception as e:
        print(f"Ошибка при отправке на сервер: {e}")

    # Обновляем состояние
    final_selection = [(city, user_days.get(city, 1)) for city in route]
    await state.update_data(final_selection=final_selection)
    await state.set_state(RoutStates.FINAL_ROUTE)

    # Создание клавиатуры с кнопкой для открытия карты
    keyboard = [
        [InlineKeyboardButton(
            text="Открыть карту",
            web_app=WebAppInfo(url="https://mabustfc.github.io/Tg-bot-TripMaster")
        )]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    # Отправка сообщения с кнопкой
    await callback_query.message.edit_text(
        "Маршрут сохранен! Нажмите кнопку, чтобы открыть карту:",
        reply_markup=reply_markup
    )
    await callback_query.answer()
