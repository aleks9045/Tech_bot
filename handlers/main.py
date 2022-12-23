from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from Data import config
from database import db
from start_bot import dp, bot
from keyboards import kb
from states.state import *
from functions.old_mode_ifs import process_callback_btn_delete1

import pickle
from nltk import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
import pymorphy2
import pandas as pd

with open(r'C:\Users\aleks\PycharmProjects\BBProgBot\pkl\model5.pkl', "rb") as f:
    model = pickle.load(f)

tokenizer = RegexpTokenizer(r'\w+')
morph = pymorphy2.MorphAnalyzer()
tfidfconverter = TfidfVectorizer()

data = pd.read_csv(r'C:\Users\aleks\PycharmProjects\BBProgBot\handlers\translated_data2.csv')
X_train = tfidfconverter.fit_transform(data["utterance"]).toarray()


@dp.message_handler(state='*', commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, f"👋 Здравствуйте, <b>{message.from_user.first_name}</b>, я - бот, "
                                                 f"созданный, чтобы помогать вам с вашими <b>вопросами</b>.\n\n"
                                                 f"🤖 <b>Бот</b> умеет отвечать на <b>вопросы</b>, связанные с <b>темами</b>:\n\n"
                                                 f"🔹 <em>Создание, удаление, редактирование</em>\n"
                                                 f"🔹 <em>Смена аккаунта, восстановление, изменение пароля</em>\n"
                                                 f"🔹 <em>Проверка оплаты, связь с тех-поддержкой и оператором, опции и сроки</em>\n"
                                                 f"🔹 <em>Доставки, жалоба, отзыв, проверка счета, получение чека</em>\n"
                                                 f"🔹 <em>Отмена, отслеживание, размещение заказа, способы и проблемы с оплатой</em>\n"
                                                 f"🔹 <em>Возврат, адрес доставки</em>\n\n"
                                                 f"🆘 Введите /help , чтобы узнать <b>функционал</b> бота.\n\n"
                                                 f"❗️ Чтобы использовать <b>новый режим</b>, вы должны <b>войти</b> в аккаунт.",
                           reply_markup=kb.main_klava, parse_mode='HTML')
    await NotLogin.state_.set()


@dp.message_handler(state='*', commands=['help'])
async def help_me(message: types.Message):
    await bot.send_message(message.from_user.id, f"📜 <b>Список команд:</b>\n\n"
                                                 f"/login — Команда входа в свой аккаунт.\n"
                                                 f"/logout — Команда выхода из своего аккаунта.\n"
                                                 f"/stop — Команда <b>остановки общения</b> с с оператором",
                           parse_mode='HTML')


@dp.callback_query_handler(lambda call: call.data == 'cancel_button', state=InChat.state_)
async def del_queue(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    if callback.from_user.id in config.operators:
        await LoginOperator.state_.set()
    else:
        await LoginUser.state_.set()
    await bot.answer_callback_query(callback.id)
    await db.delete_queue(callback.from_user.id)
    await bot.send_message(callback.from_user.id, '🚫 Поиск <b>остановлен</b>.', parse_mode='HTML')


@dp.message_handler(state=InChat.state_, commands=["stop"])
async def stop(message: types.Message, state: FSMContext):
    # try:
        chat_info = await db.get_active_chat(message.from_user.id)
        if chat_info:
            id_ = await db.vi_vishli_iz_chata(message.from_user.id)
            if message.from_user.id in config.operators:
                stated = dp.current_state(chat=message.from_user.id)
                await stated.finish()
                await stated.set_state(LoginOperator.state_)
                stated2 = dp.current_state(chat=id_)
                await stated2.finish()
                await stated2.set_state(LoginUser.state_)
                print('ОПЕРАТОР ЗАВЕРШИЛ ОБЩЕНИЕ')
            else:
                stated = dp.current_state(chat=id_)
                await stated.finish()
                await stated.set_state(LoginOperator.state_)
                stated2 = dp.current_state(chat=message.from_user.id)
                await stated2.finish()
                await stated2.set_state(LoginUser.state_)
                print('КЛИЕНТ ЗАВЕРШИЛ ОБЩЕНИЕ')

            await bot.send_message(id_, "❗️ Собеседник <b>покинул чат</b>",
                                   reply_markup=types.ReplyKeyboardRemove(),
                                   parse_mode='HTML')
            await bot.send_message(message.from_user.id, "❗️ Вы <b>вышли из чата</b>",
                                   reply_markup=types.ReplyKeyboardRemove(),
                                   parse_mode='HTML')
            await db.delete_chat(chat_info[0])
        else:
            await bot.send_message(message.from_user.id, "⚠️ Вы <b>не начали</b> чат.", parse_mode='HTML')
    # except Exception as ex_:
    #     await bot.send_message(message.from_user.id, "Произошла ошибка.")
    #     print(ex_)


@dp.message_handler(state=InChat.state_, content_types=['photo', 'text'])
async def talking(message: types.Message):
    get_active_chat = await db.check_active_chat(message.chat.id)
    if get_active_chat:
        my_id = message.from_user.id
        one = get_active_chat[1]
        two = get_active_chat[2]
        print(one, two)
        dct = {
            one: two,
            two: one
        }
        if message.text:
            await bot.send_message(dct[my_id], message.text)
        elif message.photo:
            await bot.send_photo(dct[my_id], message.photo[-1].file_id)
        else:
            pass
    else:
        pass


@dp.message_handler(state=LoginUser.state_)
async def ml(message: types.Message):
    request = message.text
    try:
        res = model.predict(tfidfconverter.transform(
            [' '.join([morph.parse(word)[0][2] for word in tokenizer.tokenize(f'{request}')])]).toarray())
        await message.answer(res[0], reply_markup=kb.bot_pomog)
    except Exception as ex_:
        print(ex_)


@dp.callback_query_handler(lambda call: call.data == 'pomog', state=LoginUser.state_)
async def pomog(callback: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback.id)
    await bot.send_message(callback.from_user.id, '❤️ Спасибо, что пользуетесь нашими услугами!\n\n'
                                                  'Не забудьте посетить социальные сети :)\n',
                           reply_markup=kb.ssilka)
    await state.finish()
    await bot.send_message(callback.from_user.id, 'Чтобы воспользоваться новым режимом снова, авторизуйтесь')
    await NotLogin.state_.set()


@dp.callback_query_handler(lambda call: call.data == 'to_operator', state=LoginUser.state_)
async def to_operator(callback: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback.id)
    chat_two = await db.get_chat(callback.from_user.id)
    if not await db.create_chat(callback.from_user.id, chat_two):
        await db.add_queue(callback.from_user.id)
        await bot.send_message(callback.from_user.id, f"🔎 Поиск <b>доступного</b> оператора...",
                               reply_markup=kb.cancel_search,
                               parse_mode='HTML')
        await state.finish()
        await InChat.state_.set()
    else:
        await state.finish()
        await InChat.state_.set()
        await bot.send_message(chat_two, "✅ Клиент <b>найден</b>!\n", reply_markup=kb.stop, parse_mode='HTML')
        await bot.send_message(callback.from_user.id, "✅ Оператор <b>найден!</b>\n"
                                                      "Начинайте общение.", parse_mode='HTML', reply_markup=kb.stop)


@dp.message_handler(state=LoginOperator.state_, commands=["find"])
async def find(message: types.Message, state: FSMContext):
    chat_two = await db.get_chat(message.chat.id)
    if not await db.create_chat(message.chat.id, chat_two):
        await db.add_queue(message.from_user.id)
        await bot.send_message(message.chat.id, f"🔎 Поиск <b>доступного</b> клиента...", reply_markup=kb.cancel_search,
                               parse_mode='HTML')
        await state.finish()
        await InChat.state_.set()
    else:
        await state.finish()
        await InChat.state_.set()
        await bot.send_message(message.chat.id, "✅ Клиент <b>найден!</b>", reply_markup=kb.stop,
                               parse_mode='HTML')
        await bot.send_message(chat_two, "✅ Оператор <b>найден!</b>", reply_markup=kb.stop,
                               parse_mode='HTML')


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


@dp.callback_query_handler(lambda call: call.data == 'old_button', state='*')
async def old_mode(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, '✅Включён старый режим.\n\nВопрос по какой теме вас интересует?',
                           reply_markup=kb.old)


def register_handlers_main(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(help_me, commands=['help'])
    dp.register_message_handler(stop, commands=['stop'])
    dp.register_message_handler(login, commands=['login'])
    dp.register_message_handler(logout_admin, commands=['logout'])
    dp.register_message_handler(logout_operator, commands=['logout'])
    dp.register_message_handler(logout, commands=['logout'])
    dp.register_message_handler(find, commands=['find'])
    dp.register_message_handler(admin_add, commands=['add'])
    dp.register_message_handler(admin_remove, commands=['remove'])
    dp.register_message_handler(ml)
    dp.register_message_handler(talking)
    dp.register_callback_query_handler(to_operator)
    dp.register_callback_query_handler(process_callback_btn_delete1)
    dp.register_callback_query_handler(process_callback_btn_delete1)
    dp.register_callback_query_handler(old_mode)
    dp.register_callback_query_handler(pomog)
    dp.register_callback_query_handler(ml)
