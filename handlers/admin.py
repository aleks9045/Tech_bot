from aiogram import types, Dispatcher

from Data import config
from database import db
from start_bot import dp
from keyboards import kb
from states.state import *


@dp.message_handler(state=LoginAdmin.state_, commands=["add"])
async def admin_add(message: types.Message):
    chat_id = message.text.split()[1]
    if chat_id in config.operators:
        await message.reply('⚠️ Оператор с таким id уже есть в базе.')
    else:
        config.operators.append(chat_id)
        await db.add_operator(chat_id)
        await message.answer('✅ Вы успешно добавили нового оператора.')


@dp.message_handler(state=LoginAdmin.state_, commands=["remove"])
async def admin_remove(message: types.Message):
    chat_id = message.text.split()[1]

    if chat_id in config.operators:
        config.operators.remove(chat_id)
        await db.del_operator(chat_id)
        await message.answer('✅ Вы успешно удалили оператора.')
    else:
        await message.reply('⚠️ Оператора с таким id нет в базе.')


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin_add, commands=['add'])
    dp.register_message_handler(admin_remove, commands=['remove'])