from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from handlers.utils.keyboards import get_greetings_keyboard
from handlers.utils.answer import GREETING_MESSAGE

from database.database_manager import add_user

router = Router()

@router.message(Command("start"))
async def auth_handler(message: types.Message, state: FSMContext):
    user_name = message.from_user.first_name
    tg_id = message.from_user.id

    await state.update_data(tg_id=tg_id)

    await add_user(tg_id)
    await message.answer_photo(
        photo = FSInputFile("img/logoTrip.png"),
        caption=GREETING_MESSAGE.format(user_name=user_name),
        parse_mode="Markdown",
        reply_markup=await get_greetings_keyboard(),
    )