from aiogram import (
    Router,
    types,
)
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery


from handlers.utils.answer import BALANCE_MESSAGE
from handlers.utils.keyboards import (
    get_balance_keyboard,
    get_greetings_keyboard
)
from database.database_manager import update_balance

router = Router()

@router.callback_query(lambda c: c.data == "balance")
async def balance_handler(callback_query: CallbackQuery):
    await callback_query.message.answer_photo(
        caption=BALANCE_MESSAGE,
        parse_mode="Markdown",
        photo=types.FSInputFile("img/balance.png"),
        reply_markup=await get_balance_keyboard()
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data.startswith("add_10_tokens") or c.data.startswith("add_20_tokens") or c.data.startswith("add_50_tokens"))
async def balance_update_handler(callback_query: CallbackQuery, state: FSMContext):
    tg_id = callback_query.from_user.id

    if tg_id is None:
        await callback_query.message.reply("Ошибка: пользователь не аутентифицирован.")
        return

    amount = 0

    if callback_query.data.startswith("add_10_tokens"):
        amount = 10

    elif callback_query.data.startswith("add_20_tokens"):
        amount = 20

    elif callback_query.data.startswith("add_50_tokens"):
        amount = 50

    await update_balance(tg_id, amount)
    await callback_query.message.answer(
        text = f"Ваш баланс пополнен на {amount} единиц.",
        parse_mode="Markdown",
        reply_markup=await get_greetings_keyboard(),
    )

    await callback_query.answer()


