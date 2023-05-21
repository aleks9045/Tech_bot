from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from Data import config
from database import db
from bot import dp, bot
from keyboards import kb
from states.state import *


@dp.message_handler(state=NotLogin.state_, commands=["login"])
async def login(message: types.Message, state: FSMContext):
    await state.finish()
    config.operators = await db.get_all_operators()
    if message.from_user.id in config.operators:
        await LoginOperator.state_.set()
        await message.answer('✅ Вы зарегистрировались как оператор.')
    elif message.from_user.id in config.admins:
        await LoginAdmin.state_.set()
        await message.answer('✅ Вы зарегистрировались как админ.\n\n'
                             '/add id_пользователя - Добавление опрератора.\n'
                             '/remove id_пользователя - Удаление опрератора.')
    else:
        await RegisterUser.state_.set()
        if message.from_user.id in await db.get_all_users_id():
            info = await db.get_all_users_info(message.from_user.id)
            await message.answer(f'✔️С возвращением, {info[0][2]}', reply_markup=kb.classes)
            await state.finish()
            await LoginUser.state_.set()
        else:
            await message.answer(f"Напишите в каком классе вы учитесь.\nНапример: '10A'")


@dp.message_handler(state=RegisterUser.state_)
async def register(message: types.Message, state: FSMContext):
    data = message.text.upper()
    name = message.from_user.first_name
    if len(data) > 3:
        await message.answer(' ❗ Произошла ошибка, попробуйте еще раз')
    else:
        await db.new_user(message.from_user.id, data, name)
        await message.answer('✅ Вы успешно зарегистрировались.\nУзнайте расписание с помощью кнопок ниже.', reply_markup=kb.classes)
        await state.finish()
        await LoginUser.state_.set()


@dp.message_handler(state=LoginUser.state_, commands=["me"])
async def me(message: types.Message, state: FSMContext):
    info = await db.get_all_users_info(message.from_user.id)
    await message.answer(f' 🛂 Ваш телеграм-айди: {info[0][0]}\n'
                         f'Ваш класс: {info[0][1]}\n'
                         f'Ваше имя: {info[0][2]}\n\n'
                         f'Изменить информацию вы можете нажав на кнопку ниже.', reply_markup=kb.change)


@dp.callback_query_handler(lambda call: call.data == 'change', state=LoginUser.state_)
async def start_change(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await ChangeUser.class_.set()
    await bot.send_message(callback.from_user.id, 'Введите класс, введите "нет", если не хотите менять информацию.')
    await callback.answer()


@dp.message_handler(state=ChangeUser.class_)
async def change_class(message: types.Message, state: FSMContext):
    data = message.text
    if data.lower() == 'нет':
        info = await db.get_all_users_info(message.from_user.id)
        await state.update_data(class_=info[0][1])
        await ChangeUser.next()
        await message.answer('Теперь введите имя.')
    elif len(data) > 3:
        await message.answer(' ❗ Произошла ошибка, попробуйте еще раз')
    else:
        await state.update_data(class_=data.upper())
        await ChangeUser.next()
        await message.answer('Теперь введите имя, введите "нет", если не хотите менять информацию.')


@dp.message_handler(state=ChangeUser.name)
async def change_name(message: types.Message, state: FSMContext):
    data = message.text
    if data.lower() == 'нет':
        info = await db.get_all_users_info(message.from_user.id)
        await state.update_data(name=info[0][2])
        state_data = await state.get_data()
        await db.change_user_info(state_data['class_'], state_data['name'], message.from_user.id)
        await state.finish()
        await LoginUser.state_.set()
        await message.answer('Информация изменена -> /me')
    else:
        await state.update_data(name=data)
        state_data = await state.get_data()
        await db.change_user_info(state_data['class_'], state_data['name'], message.from_user.id)
        await state.finish()
        await LoginUser.state_.set()
        await message.answer('Информация изменена -> /me')


@dp.message_handler(state=LoginOperator.state_, commands=["logout"])
async def logout_operator(message: types.Message, state: FSMContext):
    await state.finish()
    await NotLogin.state_.set()
    await message.answer('⚠️ Вы вышли из своего аккаунта.', reply_markup=kb.ReplyKeyboardRemove())


@dp.message_handler(state=LoginAdmin.state_, commands=["logout"])
async def logout_admin(message: types.Message, state: FSMContext):
    await state.finish()
    await NotLogin.state_.set()
    await message.answer('⚠️ Вы вышли из своего аккаунта.', reply_markup=kb.ReplyKeyboardRemove())


@dp.message_handler(state=LoginUser.state_, commands=["logout"])
async def logout(message: types.Message, state: FSMContext):
    await state.finish()
    await NotLogin.state_.set()
    await message.answer('⚠️ Вы вышли из своего аккаунта.', reply_markup=kb.ReplyKeyboardRemove())


def register_handlers_log_in_out(dp: Dispatcher):
    dp.register_message_handler(login, commands=['login'])
    dp.register_message_handler(logout_admin, commands=['logout'])
    dp.register_message_handler(logout_operator, commands=['logout'])
    dp.register_message_handler(logout, commands=['logout'])