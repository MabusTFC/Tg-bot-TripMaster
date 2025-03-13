from datetime import datetime
from calendar import monthrange

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from aiogram.utils.keyboard import InlineKeyboardBuilder

async def get_greetings_keyboard():
    inline_kb_list = [
        [InlineKeyboardButton(text="Инструкция", callback_data="manual")],
        [InlineKeyboardButton(text="Создать маршрут", callback_data="create_trip")],
        [InlineKeyboardButton(text="Пополнить баланс", callback_data="balance")],
        [InlineKeyboardButton(text="Настройка Календаря событий", callback_data="settings_calendar")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def get_support_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="Техническая поддержка", callback_data="support")
    return kb.adjust(1).as_markup()


async def get_calendar_keyboard(year: int = None, month: int = None) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    today = datetime.now()
    current_year, current_month, current_day = today.year, today.month, today.day

    if year is None:
        year = today.year
    if month is None:
        month = today.month

    first_day_weekday, days_in_month = monthrange(year, month)
    first_day_weekday = first_day_weekday % 7

    prev_month = 12 if month == 1 else month - 1
    next_month = 1 if month == 12 else month + 1
    prev_year = year - 1 if month == 1 else year
    next_year = year + 1 if month == 12 else year

    keyboard.row(
        InlineKeyboardButton(text="←", callback_data=f"change_month-{prev_year}-{prev_month:02d}"),
        InlineKeyboardButton(text=f"{month:02d}-{year}", callback_data="ignore"),
        InlineKeyboardButton(text="→", callback_data=f"change_month-{next_year}-{next_month:02d}"),
    )

    days_of_week = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    keyboard.row(*[InlineKeyboardButton(text=day, callback_data="ignore") for day in days_of_week])

    week_row = []
    for _ in range(first_day_weekday):
        week_row.append(InlineKeyboardButton(text="-", callback_data="ignore"))

    for day in range(1, days_in_month + 1):
        date_str = f"{year}-{month:02d}-{day:02d}"
        week_row.append(
            InlineKeyboardButton(text=f"{day:02d}", callback_data=f"date_{date_str}")
        )

        if len(week_row) == 7:
            keyboard.row(*week_row)
            week_row = []

    while len(week_row) < 7:
        week_row.append(InlineKeyboardButton(text="-", callback_data="ignore"))
    if any(button.text != "-" for button in week_row):
        keyboard.row(*week_row)

    keyboard.row(InlineKeyboardButton(text="Вернуться в Меню", callback_data="menu"))
    return keyboard.as_markup(resize_keyboard=True, one_time_keyboard=True)


async def get_selection_keyboard():
    inline_kb_list = [
        [InlineKeyboardButton(text="Выгодный по стоимости вариант", callback_data="benefit_cost")],
        [InlineKeyboardButton(text="Оптимальный по времени вариант", callback_data="benefit_time")],
        [InlineKeyboardButton(text="Ввести вручную промежуточные города", callback_data="hands_input")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


async def get_list_sity_keyboard(route: list, page: int = 0):
    cities_per_page = 5
    total_pages = (len(route) - 1) // cities_per_page + 1

    start_idx = page * cities_per_page
    end_idx = start_idx + cities_per_page
    cities_on_page = route[start_idx:end_idx]

    buttons = [[InlineKeyboardButton(text=city, callback_data=f"city_{start_idx + i}")] for i, city in
               enumerate(cities_on_page)]

    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅ Назад", callback_data=f"page_{page - 1}"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton(text="Вперед ➡", callback_data=f"page_{page + 1}"))

    if nav_buttons:
        buttons.append(nav_buttons)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

