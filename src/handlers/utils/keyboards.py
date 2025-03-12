
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from aiogram.utils.keyboard import InlineKeyboardBuilder

async def get_greetings_keyboard():
    inline_kb_list = [
        [InlineKeyboardButton(text="Инструкция", callback_data="manual")],
        [InlineKeyboardButton(text="Создать маршрут", callback_data="create_route")],
        [InlineKeyboardButton(text="Пополнить баланс", callback_data="balance")],
        [InlineKeyboardButton(text="Настройка Календаря событий", callback_data="settings_calendar")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def get_support_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="Техническая поддержка", callback_data="support")
    return kb.adjust(1).as_markup()
