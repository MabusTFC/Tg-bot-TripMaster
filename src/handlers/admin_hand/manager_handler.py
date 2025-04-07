import os

from aiogram import (
    Router,
    F,
)
from aiogram.types import (
    Message,
    FSInputFile
)

from handlers.utils.state_machine import (
    ManagerState,
    AdminState
)

from graph_service.graph_service import (
    new_users_graph,
    statistic_citys_graph,
)

from database.database_manager import get_user_role_from_manager

router = Router()

@router.message(F.text == "График новых пользователей", ManagerState.MANAGER_STATE)
@router.message(F.text == "График новых пользователей", AdminState.ADMIN_STATE)
async def new_user_graphic_handler(message: Message):
    username = message.from_user.username
    role = await get_user_role_from_manager(username)

    if role not in ["manager", "admin"]:
        await message.answer("❌ У вас нет доступа к этой функции.")
        return

    graph_path = await new_users_graph()
    await message.answer_photo(
        photo=FSInputFile(graph_path),
        caption="График новых пользователей"
    )
    os.remove(graph_path)


@router.message(F.text == "График популярности городов", ManagerState.MANAGER_STATE)
@router.message(F.text == "График популярности городов", AdminState.ADMIN_STATE)
async def workload_graphic_handler(message: Message):
    username = message.from_user.username
    role = await get_user_role_from_manager(username)

    if role not in ["manager", "admin"]:
        await message.answer("❌ У вас нет доступа к этой функции.")
        return

    graph_path = await statistic_citys_graph()
    await message.answer_photo(
        photo=FSInputFile(graph_path),
        caption="График популярности городов"
    )
    os.remove(graph_path)

