from aiogram.filters.state import StatesGroup, State

class RegForm(StatesGroup):
    price = State()
    amount = State()
    banks = State()
    currency = State()
    dimension =State()

class SecurityState(StatesGroup):
    password = State()

