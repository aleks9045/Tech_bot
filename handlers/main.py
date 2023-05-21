from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from Data import config
from database import db
from bot import dp, bot
from keyboards import kb
from states.state import *


@dp.message_handler(state='*', commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, f"👋 Здравствуйте, <b>{message.from_user.first_name}</b>\n"
                                                 f"Введите /help , чтобы узнать функционал бота.", parse_mode='HTML')


@dp.message_handler(state='*', commands=['help'])
async def help_me_help(message: types.Message):
    await bot.send_message(message.from_user.id, f"📜 Список команд:\n\n"
                                                 f"/login — Команда входа в свой аккаунт.\n"
                                                 f"/logout — Команда выхода из своего аккаунта.\n"
                                                 f"/me — Информация о вашем аккаунте\n"
                                                 f"/rm — Скрыть дополнительную клавиатуру\n"
                                                 f"/all_week — Расписание на неделю\n"
                                                 f"/today — Расписание на сегодня\n"
                                                 f"/other — Другие функции бота\n\n"
                                                 f"Предложения по улучшению бота? Пишите https://t.me/alisaaaaalisaaa")


@dp.message_handler(state='*', commands=["rm"])
async def logout_operator(message: types.Message, state: FSMContext):
    await message.answer(f'⌨️Клавиатура скрыта', reply_markup=kb.ReplyKeyboardRemove())


def register_handlers_main(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(help_me_help, commands=['help'])
