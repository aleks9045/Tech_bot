from start_bot import dp, bot
from aiogram import types
from keyboards import kb


@dp.callback_query_handler(lambda call: call.data and call.data.startswith('key_'), state='*')
async def process_callback_btn_delete1(callback_query: types.CallbackQuery):
    if callback_query.data.split('key_')[1] == 'account':
        await bot.send_message(callback_query.from_user.id, text='👤 Проблемы с <b>аккаунтом</b> ⁉️',
                               reply_markup=kb.accounts, parse_mode='HTML')
    elif callback_query.data.split('key_')[1] == 'contact':
        await bot.send_message(callback_query.from_user.id, text='📞 Наши <b>контакты</b>',
                               reply_markup=kb.contacts, parse_mode='HTML')
    elif callback_query.data.split('key_')[1] == 'deliver':
        await bot.send_message(callback_query.from_user.id, text='🚚 Проблемы с <b>доставкой</b> ⁉️',
                               reply_markup=kb.delivers, parse_mode='HTML')
    elif callback_query.data.split('key_')[1] == 'feedback':
        await bot.send_message(callback_query.from_user.id, text='🧑‍💻 <b>Обратную связь</b> можно осуществить ниже',
                               reply_markup=kb.feedbacks, parse_mode='HTML')
    elif callback_query.data.split('key_')[1] == 'check':
        await bot.send_message(callback_query.from_user.id, text='📃 Всё о <b>чеках</b>',
                               reply_markup=kb.checks, parse_mode='HTML')
    elif callback_query.data.split('key_')[1] == 'order':
        await bot.send_message(callback_query.from_user.id, text='📦 Всё о <b>заказах</b>',
                               reply_markup=kb.orders, parse_mode='HTML')
    elif callback_query.data.split('key_')[1] == 'payment':
        await bot.send_message(callback_query.from_user.id, text='💳 Всё об <b>оплате</b>',
                               reply_markup=kb.payments, parse_mode='HTML')
    elif callback_query.data.split('key_')[1] == 'refund':
        await bot.send_message(callback_query.from_user.id, text='💸 Всё о <b>возвратах</b>',
                               reply_markup=kb.refunds, parse_mode='HTML')


@dp.callback_query_handler(lambda call: call.data and call.data.startswith('btn_'), state='*')
async def process_callback_btn_delete2(callback_query: types.CallbackQuery):
    if callback_query.data.split('btn_')[1] == 'create':
        await bot.send_message(callback_query.from_user.id, text='➕ Чтобы <b>создать аккаунт</b>, <b>создайте '
                                                                 'аккаунт</b>',
                               parse_mode='HTML')
    elif callback_query.data.split('btn_')[1] == 'delete':
        await bot.send_message(callback_query.from_user.id,
                               text='❌ Чтобы <b>удалить аккаунт</b>, <b>удалите аккаунт</b>',
                               parse_mode='HTML')
    elif callback_query.data.split('btn_')[1] == 'edit':
        await bot.send_message(callback_query.from_user.id,
                               text='✏️ Чтобы <b>редактировать аккаунт</b>, <b>редактируйте аккаунт</b>',
                               parse_mode='HTML')
    elif callback_query.data.split('btn_')[1] == 'recover':
        await bot.send_message(callback_query.from_user.id,
                               text='🔐 Чтобы <b>восстановить пароль</b>, <b>восстановите пароль</b>',
                               parse_mode='HTML')
    elif callback_query.data.split('btn_')[1] == 'switch':
        await bot.send_message(callback_query.from_user.id,
                               text='🔄 Чтобы <b>сменить аккаунт</b>, <b>смените аккаунт</b>',
                               parse_mode='HTML')
    elif callback_query.data.split('btn_')[1] == 'support':
        await bot.send_message(callback_query.from_user.id,
                               text='🛠 Чтобы <b>обратиться в тех.поддержку</b>, <b>обратитесь</b>',
                               parse_mode='HTML')
    elif callback_query.data.split('btn_')[1] == 'human':
        await bot.send_message(callback_query.from_user.id,
                               text='🧑‍💻 Чтобы <b>обратиться к оператору</b>, <b>обратитесь</b>',
                               parse_mode='HTML')
    elif callback_query.data.split('btn_')[1] == 'options':
        await bot.send_message(callback_query.from_user.id, text='🚚 <b>Варианты доставки</b> следующие:',
                               parse_mode='HTML')
    elif callback_query.data.split('btn_')[1] == 'period':
        await bot.send_message(callback_query.from_user.id, text='📅 <b>Сроки доставки</b> следующие:',
                               parse_mode='HTML')
    elif callback_query.data.split('btn_')[1] == 'complaint':
        await bot.send_message(callback_query.from_user.id, text='📔 <b>Жалобу</b> можно оформить так:',
                               parse_mode='HTML')
    elif callback_query.data.split('btn_')[1] == 'review':
        await bot.send_message(callback_query.from_user.id, text='📚 <b>Отзыв</b> можно оформить так:',
                               parse_mode='HTML')
    elif callback_query.data.split('btn_')[1] == 'get':
        await bot.send_message(callback_query.from_user.id,
                               text='📃 Чтобы <b>получить</b> чек заказа, <b>получите его</b>',
                               parse_mode='HTML')
    elif callback_query.data.split('btn_')[1] == 'cancel':
        await bot.send_message(callback_query.from_user.id, text='❌ Чтобы <b>отменить заказ</b>, <b>отмените его</b>',
                               parse_mode='HTML')
    elif callback_query.data.split('btn_')[1] == 'place':
        await bot.send_message(callback_query.from_user.id,
                               text='📝 Чтобы <b>разместить объявление</b>, <b>разместите его</b>',
                               parse_mode='HTML')
    elif callback_query.data.split('btn_')[1] == 'track0':
        await bot.send_message(callback_query.from_user.id, text='👁 Чтобы <b>отследить заказ</b>, <b>отследите его</b>',
                               parse_mode='HTML')
    elif callback_query.data.split('btn_')[1] == 'method':
        await bot.send_message(callback_query.from_user.id, text='💳 Доступные <b>способы</b> оплаты:',
                               parse_mode='HTML')
    elif callback_query.data.split('btn_')[1] == 'issue':
        await bot.send_message(callback_query.from_user.id, text='📚 Возможные <b>решения проблемы</b>',
                               parse_mode='HTML')
    elif callback_query.data.split('btn_')[1] == 'policy':
        await bot.send_message(callback_query.from_user.id, text='📜 Политика <b>возвратов</b> такова',
                               parse_mode='HTML')
    elif callback_query.data.split('btn_')[1] == 'got':
        await bot.send_message(callback_query.from_user.id, text='💸 Чтобы <b>оформить возврат</b> нужно',
                               parse_mode='HTML')
    elif callback_query.data.split('btn_')[1] == 'track1':
        await bot.send_message(callback_query.from_user.id, text='👁 Чтобы <b>отследить возврат</b> нужно',
                               parse_mode='HTML')