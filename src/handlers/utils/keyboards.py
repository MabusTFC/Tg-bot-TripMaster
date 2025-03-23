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
        [InlineKeyboardButton(text="Поолнить баланс", callback_data="balance")],
        [InlineKeyboardButton(text="Календарь", callback_data="g_calendar")],
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
        [InlineKeyboardButton(text="Найти наиболее подходящий маршрут из списка городов", callback_data="benefit_rout")],
        [InlineKeyboardButton(text="Ввести вручную промежуточные города итогового маршрута", callback_data="hands_input")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


async def get_list_sity_keyboard(route: list, user_days: dict, page: int = 0):
    cities_per_page = 5
    total_pages = (len(route) - 1) // cities_per_page + 1

    start_idx = page * cities_per_page
    end_idx = start_idx + cities_per_page
    cities_on_page = route[start_idx:end_idx]

    buttons = []
    for i, city in enumerate(cities_on_page):
        city_index = start_idx + i
        days = user_days.get(city, None)
        text = f"{city} ({days}д)" if days else city
        buttons.append([InlineKeyboardButton(text=text, callback_data=f"select_{city_index}")])

    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅ Назад", callback_data=f"page_{page - 1}"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton(text="Вперед ➡", callback_data=f"page_{page + 1}"))

    if nav_buttons:
        buttons.append(nav_buttons)

    buttons.append([InlineKeyboardButton(text="✅ Готово", callback_data="finish_selection")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def get_days_keyboard(city: str, days: int, max_days: int):
    """Клавиатура для изменения количества дней"""
    increase_button = InlineKeyboardButton(
        text="➕" if days < max_days else "🔒",
        callback_data=f"increase_{city}" if days < max_days else "lock"
    )

    buttons = [
        [InlineKeyboardButton(text="➖", callback_data=f"decrease_{city}"),
         InlineKeyboardButton(text=f"{days} дн", callback_data="current_days"),
         increase_button],
        [InlineKeyboardButton(text="✅ Готово", callback_data="back_to_cities")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def get_number_keyboard(city: str, current_days: int, max_days: int):
    buttons = [
        InlineKeyboardButton(text=f"{i}дн", callback_data=f"choose_number|{city}|{i}") for i in range(1, max_days + 1)
    ]

    rows = [buttons[i:i + 7] for i in range(0, len(buttons), 7)]

    return InlineKeyboardMarkup(inline_keyboard=rows)


async def get_zveno_rout_keyboard(days: int, max_days: int):
    increase_button = InlineKeyboardButton(
        text="➕" if days < max_days else "🔒",
        callback_data="pluse_days" if days < max_days else "locked"
    )

    buttons = [
        [InlineKeyboardButton(text="Создать ещё звено", callback_data="add_zveno")],
        [InlineKeyboardButton(text="➖", callback_data="minus_days"),
         InlineKeyboardButton(text=f"{days} дн", callback_data="current_days_zveno"),
         increase_button],
        [InlineKeyboardButton(text="✅ Готово", callback_data="save_zveno")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)

async def get_google_calendar_keyboard():
    buttons = [
        [InlineKeyboardButton(text="Авторизация гугл", callback_data="authorization")],
        [InlineKeyboardButton(text="Добавить путешествие в календарь", callback_data="add_event")],
        [InlineKeyboardButton(text="Распечатать поездку", callback_data="print_calendar")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
