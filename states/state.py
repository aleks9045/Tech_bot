from aiogram.dispatcher.filters.state import State, StatesGroup


class LoginOperator(StatesGroup):
    state_ = State()


class RegisterUser(StatesGroup):
    state_ = State()


class ChangeUser(StatesGroup):
    class_ = State()
    name = State()


class LoginUser(StatesGroup):
    state_ = State()


class LoginAdmin(StatesGroup):
    state_ = State()


class NotLogin(StatesGroup):
    state_ = State()


class Rus_test(StatesGroup):
    first = State()
    second = State()
    third = State()