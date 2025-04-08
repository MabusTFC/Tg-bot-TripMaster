import datetime
import requests
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
)
from handlers.utils.answer import SUPPORT_TEH_MESS  # Добавлен импорт

from src.handlers.utils.answer import GUIDE_MESSAGE,SUPPORT_TEH_MESS

router = Router()


@router.callback_query(lambda c: c.data == "support")
async def authorization_google(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer(
        text=SUPPORT_TEH_MESS,
        parse_mode="MarkdownV2"  # Используем MarkdownV2 для форматирования
    )
    await callback_query.answer()  # Закрываем уведомление о нажатии


@router.callback_query(lambda c: c.data == "guide")
async def authorization_google(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer(
        text=GUIDE_MESSAGE,
        parse_mode="MarkdownV2"  # Используем MarkdownV2 для форматирования
    )
    await callback_query.answer()  # Закрываем уведомление о нажатии