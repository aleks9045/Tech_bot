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
                                                 f"Чтобы пользоваться ботом, нужно загеристрироваться.\n"
                                                 f"Введите /help , чтобы узнать <b>функционал</b> бота.", parse_mode='HTML')
    await NotLogin.state_.set()


@dp.message_handler(state='*', commands=['help'])
async def help_me_help(message: types.Message):
    await bot.send_message(message.from_user.id, f"📜 Список команд:\n\n"
                                                 f"/login — Команда входа в свой аккаунт.\n"
                                                 f"/logout — Команда выхода из своего аккаунта.\n"
                                                 f"/stop — Команда остановки общения.\n"
                                                 f"/help_me - Команда поиска оператора(для клиентов)."
                                                 f"/find - Команда поиска клиента(для операторов).")


@dp.message_handler(state=LoginUser.state_, commands=['help_me'])
async def help_me(message: types.Message, state: FSMContext):
    chat_two = await db.get_chat(message.from_user.id)
    if not await db.create_chat(message.from_user.id, chat_two):
        await db.add_queue(message.from_user.id)
        await bot.send_message(message.from_user.id, f"🔎 Поиск <b>доступного</b> оператора...",
                               reply_markup=kb.cancel_search,
                               parse_mode='HTML')
        await state.finish()
        await InChat.state_.set()
        # await InSearch.state_.set()
    else:
        await state.finish()
        await InChat.state_.set()

        # stated2 = dp.current_state(chat=chat_two)
        # await stated2.finish()
        # await stated2.set_state(InChat.state_)

        await bot.send_message(chat_two, "✅ Клиент <b>найден</b>!\n", reply_markup=kb.stop, parse_mode='HTML')
        await bot.send_message(message.from_user.id, "✅ Оператор <b>найден!</b>\n"
                                                      "Начинайте общение.", parse_mode='HTML', reply_markup=kb.stop)


@dp.message_handler(state=LoginOperator.state_, commands=["find"])
async def find(message: types.Message, state: FSMContext):
    chat_two = await db.get_chat(message.chat.id)
    if not await db.create_chat(message.chat.id, chat_two):
        await db.add_queue(message.from_user.id)
        await bot.send_message(message.chat.id, f"🔎 Поиск доступного <b>клиента</b>...", reply_markup=kb.cancel_search,
                               parse_mode='HTML')
        await state.finish()
        await InChat.state_.set()
        # await InSearch.state_.set()
    else:
        await state.finish()
        await InChat.state_.set()

        # stated2 = dp.current_state(chat=chat_two)
        # await stated2.finish()
        # await stated2.set_state(InChat.state_)

        await bot.send_message(message.chat.id, "✅ Клиент <b>найден!</b>", reply_markup=kb.stop,
                               parse_mode='HTML')
        await bot.send_message(chat_two, "✅ Оператор <b>найден!</b>", reply_markup=kb.stop,
                               parse_mode='HTML')


@dp.callback_query_handler(lambda call: call.data == 'cancel_button', state=InChat.state_)
async def del_queue(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    if callback.from_user.id in config.operators:
        await LoginOperator.state_.set()
        await bot.send_message(callback.from_user.id, '🚫 Поиск <b>остановлен</b>.', parse_mode='HTML',
                               reply_markup=kb.find)
    else:
        await LoginUser.state_.set()
        await bot.send_message(callback.from_user.id, '🚫 Поиск <b>остановлен</b>.', parse_mode='HTML')
    await bot.answer_callback_query(callback.id)
    await db.delete_queue(callback.from_user.id)


@dp.message_handler(state=InChat.state_, commands=["stop"])
async def stop(message: types.Message, state: FSMContext):
    try:
        chat_info = await db.get_active_chat(message.from_user.id)
        if chat_info:
            id_ = await db.vi_vishli_iz_chata(message.from_user.id)

            await bot.send_message(id_, "❗️ Собеседник <b>покинул чат</b>",
                                   reply_markup=types.ReplyKeyboardRemove(),
                                   parse_mode='HTML')
            await bot.send_message(message.from_user.id, "❗️ Вы <b>вышли из чата</b>",
                                   reply_markup=types.ReplyKeyboardRemove(),
                                   parse_mode='HTML')

            if message.from_user.id in config.operators:
                await state.finish()
                await LoginOperator.state_.set()
                await bot.send_message(id_, "⌚ Начался атоматический поиск нового оператора...",
                                       reply_markup=kb.cancel_search,
                                       parse_mode='HTML')
            else:
                await state.finish()
                await LoginUser.state_.set()
                await bot.send_message(id_, "⌚ Начался атоматический поиск нового клиента...",
                                       reply_markup=kb.cancel_search,
                                       parse_mode='HTML')
            await db.delete_chat(chat_info[0])
        else:
            await bot.send_message(message.from_user.id, "⚠️Вы <b>не начали</b> чат.", parse_mode='HTML')
    except Exception as ex_:
        await bot.send_message(message.from_user.id, "Произошла ошибка.")
        print(ex_)


@dp.message_handler(state=InChat.state_, content_types=['photo', 'text'])
async def talking(message: types.Message):
    get_active_chat = await db.check_active_chat(message.chat.id)
    if get_active_chat:
        my_id = message.from_user.id
        one = get_active_chat[1]
        two = get_active_chat[2]
        dct = {
            one: two,
            two: one
        }
        if message.text:
            await bot.send_message(dct[my_id], message.text)
        elif message.photo:
            await bot.send_photo(dct[my_id], message.photo[-1].file_id, caption=message.caption)
        else:
            pass
    else:
        pass


def register_handlers_main(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(help_me_help, commands=['help'])
    dp.register_message_handler(stop, commands=['stop'])
    dp.register_message_handler(find, commands=['find'])
    dp.register_message_handler(talking)
    dp.register_message_handler(help_me, commands=['help_me'])
