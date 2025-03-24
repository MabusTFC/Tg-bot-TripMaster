import json
import datetime
import os

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, WebAppInfo
from aiogram.types import InputFile, InputMediaDocument,BufferedInputFile
from telegram import InlineKeyboardButton
from datetime import datetime

from Algorithm.FindCheapestWay import get_routes
from handlers.utils.keyboards import get_balance_keyboard

router = Router()

@router.callback_query(lambda c: c.data == "add_10_tokens")
async def add_10_tokens(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.bot.send_message(chat_id=callback_query.from_user.id,text="Ваш баланс увеличился на 10 ТОКЕНОВ!")

@router.callback_query(lambda c: c.data == "add_20_tokens")
async def add_20_tokens(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.bot.send_message(chat_id=callback_query.from_user.id,text="Ваш баланс увеличился на 20 ТОКЕНОВ!")

@router.callback_query(lambda c: c.data == "add_50_tokens")
async def add_50_tokens(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.bot.send_message(chat_id=callback_query.from_user.id,text="Ваш баланс увеличился на 50 ТОКЕНОВ!")