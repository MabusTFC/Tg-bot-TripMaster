from aiogram.fsm.state import (
    StatesGroup,
    State
)

class DateSelection(StatesGroup):
    START_DATE = State()
    END_DATE = State()