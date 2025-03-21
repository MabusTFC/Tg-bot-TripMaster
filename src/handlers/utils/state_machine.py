from aiogram.fsm.state import (
    StatesGroup,
    State
)

class DateSelection(StatesGroup):
    START_DATE = State()
    END_DATE = State()
    TOTAL_DAYS = State()
    MAX_STAY_DAYS = State()

class RoutStates(StatesGroup):
    SELECT_CITY = State()
    ADD_CITY = State()
    FINAL_ROUTE = State()
    ZVENO_ROUT = State()