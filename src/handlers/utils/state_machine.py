from aiogram.fsm.state import (
    StatesGroup,
    State
)

class DateSelection(StatesGroup):
    START_DATE = State()
    END_DATE = State()
    TOTAL_DAYS = State()
    MAX_STAY_DAYS = State()

class DateSelectionManager(StatesGroup):
    START_DATE = State()
    END_DATE = State()

class RoutStates(StatesGroup):
    SELECT_CITY = State()
    ADD_CITY = State()
    FINAL_ROUTE = State()
    ZVENO_ROUT = State()


class AdminState(StatesGroup):
    ADD_MANAGER_NAME = State()
    CONFIRM_ADD_MANAGER = State()
    DELETE_MANAGER_NAME = State()
    ADMIN_STATE = State()

class ManagerState(StatesGroup):
    MANAGER_STATE = State()
