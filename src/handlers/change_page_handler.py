from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.utils.keyboards import get_selection_keyboard, get_list_sity_keyboard



router = Router()

@router.callback_query(lambda c: c.data.startswith("page_"))
async def change_page(callback_query: CallbackQuery, state: FSMContext):
    page = int(callback_query.data.split("_")[1])
    user_data = await state.get_data()
    route = user_data.get("route", [])

    await callback_query.message.edit_text(text= f"Маршрут обновлен!\nГорода маршрута:\n\n" + "\n".join(route),
                                           reply_markup=await get_list_sity_keyboard(route, page)
                                           )
    await callback_query.answer()