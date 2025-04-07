from aiogram import Router, types
from aiogram.types import CallbackQuery

from handlers.utils.keyboards import get_cities_keyboard

router = Router()


@router.callback_query(lambda c: c.data == "saved_routes")
async def show_cities(callback: types.CallbackQuery):
    keyboard = await get_cities_keyboard(callback.from_user.id)

    if keyboard:
        await callback.message.answer("Сохранённые города:", reply_markup=keyboard)
    else:
        await callback.message.answer("У вас нет сохранённых маршрутов.")

    await callback.answer()

'''
    Метод для выбора города, как вариация улучшения/доработки
@router.callback_query(lambda c: c.data == "Колбэк кнопки клавиатуры")
async def city_selected(callback_query: types.CallbackQuery):
    city = callback_query.data.split("_")[1]
    await callback_query.answer(f"Вы выбрали: {city}")
    await callback_query.message.answer(f"Вы выбрали город {city}")
    
'''
