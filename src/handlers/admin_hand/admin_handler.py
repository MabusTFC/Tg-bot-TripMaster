from aiogram import (
    Router,
    F
)
from src.database.database_manager import (
    add_manager_user_by_name,
    get_all_managers_list,
    delete_manager_from_db,
)
from aiogram.types import (
    Message,
    CallbackQuery,
)
from aiogram.fsm.context import FSMContext
from handlers.utils.state_machine import AdminState

from handlers.utils.keyboards import (
    get_list_manager_keyboard,
    get_admin_keyboard,
    get_agreement_dell_keyboard
)

router = Router()

@router.message(F.text == "Добавить менеджера", AdminState.ADMIN_STATE)
async def add_manager_handler(message: Message, state: FSMContext):
    await message.answer(
        "Пожалуйста, введите имя пользователя, которого вы хотите добавить в качестве менеджера.",
        parse_mode="Markdown"
    )
    await state.set_state(AdminState.ADD_MANAGER_NAME)

@router.message(AdminState.ADD_MANAGER_NAME)
async def save_manager_name(message: Message, state: FSMContext):
    manager_name = message.text.strip()
    manager_list = await get_all_managers_list()
    await state.update_data(manager_name=manager_name)

    if manager_name not in manager_list:
        await add_manager_user_by_name(manager_name)
        await message.answer(f"✅ Менеджер {manager_name} добавлен!")
        await state.clear()
        await state.set_state(AdminState.ADMIN_STATE)
    else:
        await message.answer("Менеджер уже существует!")
        await state.clear()
        await state.set_state(AdminState.ADMIN_STATE)



@router.message(F.text == "Удалить менеджера", AdminState.ADMIN_STATE)
async def dell_manager_handler(message: Message, state: FSMContext):
    keyboard = await get_list_manager_keyboard()
    await message.answer(
        text="Выберите менеджера для удаления:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )


@router.callback_query(lambda c: c.data.startswith("delete_manager_"))
async def delete_manager_handler(callback_query: CallbackQuery):
    manager_teg = callback_query.data.replace("delete_manager_", "")

    await callback_query.message.edit_text(
        f"Подтвердите удаление менеджера {manager_teg}",
        reply_markup=await get_agreement_dell_keyboard(manager_teg),
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data.startswith("confirm_delete_"))
async def delete_manager(callback_query: CallbackQuery):
    manager_teg = callback_query.data.replace("confirm_delete_", "")

    await delete_manager_from_db(manager_teg)

    await callback_query.message.edit_text(f"✅ Менеджер {manager_teg} удален.")
    await callback_query.answer()


