from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from random import choice
from database import db
from bot import dp, bot
from keyboards import kb
from states.state import *


@dp.message_handler(state=LoginUser.state_, commands=["other"])
async def other(message: types.Message):
    await message.answer('➡️Другие функции бота', reply_markup=kb.other)


@dp.callback_query_handler(lambda call: call.data == 'tests', state=LoginUser.state_)
async def tests(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, '❔Выберите предмет', reply_markup=kb.tests)
    await callback.answer()


@dp.callback_query_handler(lambda call: call.data == 'rus', state=LoginUser.state_)
async def rus(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await Rus_test.first.set()
    tasks = await db.get_task()
    await state.update_data(first=0)
    await bot.send_message(callback.from_user.id, tasks[0][0], reply_markup=kb.ottf)
    await callback.answer()


@dp.message_handler(state=Rus_test.first)
async def first(message: types.Message, state: FSMContext):
    await Rus_test.next()
    ans = message.text
    right = await db.get_answer()
    tasks = await db.get_task()
    if ans == str(right[0][0]):
        await state.update_data(first=1)
        await message.answer('✅Верно!')
        await message.answer(tasks[0][1])
    else:

        await message.answer(f'❌Неверно! Правильный ответ был {right[0][0]}')
        await message.answer(tasks[0][1])


@dp.message_handler(state=Rus_test.second)
async def second(message: types.Message, state: FSMContext):
    await Rus_test.next()
    ans = message.text
    right = await db.get_answer()
    tasks = await db.get_task()
    if ans == str(right[0][1]):
        await state.update_data(first=2)
        await message.answer('✅Верно!')
        await message.answer(tasks[0][2])

    else:
        await message.answer(f'❌Неверно! Правильный ответ был {right[0][0]}')
        await message.answer(tasks[0][2])


@dp.message_handler(state=Rus_test.third)
async def third(message: types.Message, state: FSMContext):
    ans = message.text
    right = await db.get_answer()
    tasks = await db.get_task()
    if ans == str(right[0][2]):
        await state.update_data(first=3)
        await message.answer('Верно!')
        data = await state.get_data()
        await message.answer(f"✅✅✅Вы ответили правильно на {data['first']} вопросов из 3.", reply_markup=kb.classes)
        await state.finish()
        await LoginUser.state_.set()
    else:
        data = await state.get_data()
        await message.answer(f'❌Неверно! Правильный ответ был {right[0][0]}')
        await message.answer(f"Вы ответили правильно на {data['first']} вопросов из 3.\n"
                             f"Вы можете потренироваться на этом сайте: https://gramotei.online/demo/run", reply_markup=kb.classes)
        await state.finish()
        await LoginUser.state_.set()


@dp.callback_query_handler(lambda call: call.data == 'tips', state=LoginUser.state_)
async def tips(callback: types.CallbackQuery):
    tips = await db.get_tip()
    tip = choice(tips)[0]
    if tip.startswith('😺'):
        await bot.send_message(callback.from_user.id, tip, reply_markup=kb.more_tip)
        await bot.send_video(callback.from_user.id, open(r'C:\Users\aleks\PycharmProjects\Tech_bot\Data', 'rb'))
        await callback.answer()

    else:
        await bot.send_message(callback.from_user.id, tip, reply_markup=kb.more_tip)
        await callback.answer()


@dp.message_handler(content_types=["document"])
async def sticker_file_id(message: types.Message):
    await message.answer(f"ID документа {message.document.file_id}")


def register_handlers_shedule(dp: Dispatcher):
    dp.register_message_handler(other, commands=['other'])