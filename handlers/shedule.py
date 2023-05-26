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
        result = ''
        if weekday > 4:
            await message.answer('Сегодня выходной')
        elif weekday == 0:
            res = data.split('  ')[weekday * 2 + 1:5]
            for i in range(len(res)):
                if i % 2 != 0:
                    result += '\n'.join(res[i].split())
                else:
                    result += '\n\n----------------' + res[i] + '----------------\n\n'
            await message.answer(result)
        else:
            res = data.split('  ')[weekday * 2 + 1:weekday * 2 + 5]
            for i in range(len(res)):
                if i % 2 != 0:
                    result += '\n'.join(res[i].split())
                else:
                    result += '\n\n----------------' + res[i] + '----------------\n\n'
            await message.answer(result)





def register_handlers_shedule(dp: Dispatcher):
    dp.register_message_handler(week, commands=['all_week'])
    dp.register_message_handler(today, commands=['today'])