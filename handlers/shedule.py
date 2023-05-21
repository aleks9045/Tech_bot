from aiogram import types, Dispatcher

import datetime
from database import db
from bot import dp, bot
from keyboards import kb
from states.state import *


@dp.message_handler(state=LoginUser.state_, commands=["all_week"])
async def week(message: types.Message):
    info = await db.get_all_users_info(message.from_user.id)
    all_classes = await db.get_week_shedule()
    data = ''
    for i in all_classes:
        if info[0][1] == str(i[0]).split('  ')[0]:
            data = str(i[0])
    if data == '':
        await message.answer('Произошла ошибка, проверьте правильность введёного класса при регистрации.')
    else:
        await message.answer(data.replace(' ', '\n'))


@dp.message_handler(state=LoginUser.state_, commands=["today"])
async def today(message: types.Message):
    info = await db.get_all_users_info(message.from_user.id)
    all_classes = await db.get_week_shedule()
    data = ''
    for i in all_classes:
        if info[0][1] == str(i[0]).split('  ')[0]:
            data = str(i[0])
    if data == '':
        await message.answer('Произошла ошибка, проверьте правильность введёного класса при регистрации.')
    else:
        weekday = datetime.date.today().weekday()
        if weekday > 4:
            await message.answer('Сегодня выходной')
        else:
            res = data.split('  ')[weekday * 2 + 1:weekday * 2 + 5]
            await message.answer('\n'.join(res))


def register_handlers_shedule(dp: Dispatcher):
    dp.register_message_handler(week, commands=['all_week'])
    dp.register_message_handler(today, commands=['today'])