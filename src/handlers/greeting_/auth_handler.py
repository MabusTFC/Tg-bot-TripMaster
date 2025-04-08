from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from handlers.utils.keyboards import (
    get_greetings_keyboard,
    get_manager_keyboard,
    get_admin_keyboard
)
from handlers.utils.answer import GREETING_MESSAGE

from database.database_manager import (
    add_user,
    get_user_role_from_manager
)

from handlers.utils.state_machine import (
    AdminState,
    ManagerState
)

from src.database.database_manager import get_user_balance

router = Router()

@router.message(Command("start"))
async def auth_handler(message: types.Message, state: FSMContext):
    await state.clear()
    user_name = message.from_user.first_name
    tg_id = message.from_user.id
    name = message.from_user.username

    role = await get_user_role_from_manager(name)
    await state.update_data(tg_id=tg_id)

    await add_user(tg_id, name)
    balance = await get_user_balance(tg_id)
    await message.answer_photo(
        photo = FSInputFile("img/logoTrip.png"),
        caption=GREETING_MESSAGE.format(user_name=user_name, balance=balance),
        parse_mode="Markdown",
        reply_markup=await get_greetings_keyboard(),
    )
    if role == "manager":
        await state.set_state(ManagerState.MANAGER_STATE)
        await message.answer(
            text="_Вам доступен менеджер функционал_",
            parse_mode="Markdown",
            reply_markup=await get_manager_keyboard()
        )


    elif role == "admin":
        await state.set_state(AdminState.ADMIN_STATE)
        await message.answer(
            text="_Вам доступен админ функционал_",
            parse_mode="Markdown",
            reply_markup=await get_admin_keyboard()

        )


