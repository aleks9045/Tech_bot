from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from Data import config
from database import db
from start_bot import dp
from keyboards import kb
from states.state import *


@dp.message_handler(state=NotLogin.state_, commands=["login"])
async def login(message: types.Message, state: FSMContext):
    await state.finish()
    config.operators = await db.get_all_operators()
    if message.from_user.id in config.operators:
        await LoginOperator.state_.set()
        await message.answer('✅ Вы зарегистрировались как оператор.', reply_markup=kb.find)
    elif message.from_user.id in config.admins:
        await LoginAdmin.state_.set()
        await message.answer('✅ Вы зарегистрировались как админ.\n\n'
                             '/add id_пользователя - Добавление опрератора.\n'
                             '/remove id_пользователя - Удаление опрератора.')
    else:
        await LoginUser.state_.set()
        await message.answer('✅ Вы зарегистрировались как клиент.\n\n'
                             'Теперь вы можете изложить интересующий вас вопрос.')


@dp.message_handler(state=LoginOperator.state_, commands=["logout"])
async def logout_operator(message: types.Message, state: FSMContext):
    await state.finish()
    await NotLogin.state_.set()
    await message.answer('⚠️ Вы вышли из своего аккаунта.')


@dp.message_handler(state=LoginAdmin.state_, commands=["logout"])
async def logout_admin(message: types.Message, state: FSMContext):
    await state.finish()
    await NotLogin.state_.set()
    await message.answer('⚠️ Вы вышли из своего аккаунта.')


@dp.message_handler(state=LoginUser.state_, commands=["logout"])
async def logout(message: types.Message, state: FSMContext):
    await state.finish()
    await NotLogin.state_.set()
    await message.answer('⚠️ Вы вышли из своего аккаунта.')


def register_handlers_log_in_out(dp: Dispatcher):
    dp.register_message_handler(login, commands=['login'])
    dp.register_message_handler(logout_admin, commands=['logout'])
    dp.register_message_handler(logout_operator, commands=['logout'])
    dp.register_message_handler(logout, commands=['logout'])