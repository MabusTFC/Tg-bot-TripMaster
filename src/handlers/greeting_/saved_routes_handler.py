from aiogram import Router, types
from aiogram.types import CallbackQuery

from handlers.utils.keyboards import get_cities_keyboard

router = Router()

@router.callback_query(lambda c: c.data == "saved_routes")
async def show_cities(message: types.Message):
    keyboard = await get_cities_keyboard(message.from_user.id)
    if keyboard:
        await message.answer("Cохраненные города", reply_markup=keyboard)
    else:
        await message.answer("У вас нет сохранённых маршрутов.")

'''
    Метод для выбора города, как вариация улучшения/доработки
@router.callback_query(lambda c: c.data == "Колбэк кнопки клавиатуры")
async def city_selected(callback_query: types.CallbackQuery):
    city = callback_query.data.split("_")[1]
    await callback_query.answer(f"Вы выбрали: {city}")
    await callback_query.message.answer(f"Вы выбрали город {city}")
    
'''
