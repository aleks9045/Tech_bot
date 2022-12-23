from aiogram.dispatcher.filters.state import State, StatesGroup


class LoginOperator(StatesGroup):
    state_ = State()


class LoginUser(StatesGroup):
    state_ = State()


class LoginAdmin(StatesGroup):
    state_ = State()


class InChat(StatesGroup):
    state_ = State()


class NotLogin(StatesGroup):
    state_ = State()
