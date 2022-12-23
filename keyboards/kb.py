from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardMarkup, KeyboardButton

main_klava = InlineKeyboardMarkup(resize_keyboard=True)
old_button = InlineKeyboardButton('Старый режим.', callback_data='old_button')
main_klava.add(old_button)


cancel_search = InlineKeyboardMarkup(resize_keyboard=True)
cancel_button = InlineKeyboardButton('Остановить поиск.', callback_data='cancel_button')
cancel_search.add(cancel_button)

stop = ReplyKeyboardMarkup(resize_keyboard=True)
stop_button = KeyboardButton('/stop')
stop.add(stop_button)

bot_pomog = InlineKeyboardMarkup(resize_keyboard=True)
pomog = InlineKeyboardButton('Бот помог мне.', callback_data='pomog')
not_pomog = InlineKeyboardButton('Обратиться в поддержку.', callback_data='to_operator')
bot_pomog.add(pomog, not_pomog)

ssilka = InlineKeyboardMarkup(resize_keyboard=True)
vk_ssilka = InlineKeyboardButton('Наше Вконтакте', url='https://vk.cc/cjOXsu', callback_data='vk')
tg_ssilka = InlineKeyboardButton('Наш Телеграмм', url='https://t.me/rksi_ru', callback_data='tg')
ssilka.add(vk_ssilka, tg_ssilka)


find = ReplyKeyboardMarkup(resize_keyboard=True)
find_button = KeyboardButton('/find')
find.add(find_button)


old = InlineKeyboardMarkup(resize_keyboard=True)
account = InlineKeyboardButton('👤 УЧЕТНАЯ ЗАПИСЬ', callback_data='key_account')
contact = InlineKeyboardButton('📞 КОНТАКТЫ', callback_data='key_contact')
deliver = InlineKeyboardButton('🚚 ДОСТАВКА', callback_data='key_deliver')
feedback = InlineKeyboardButton('💬 ОБРАТНАЯ СВЯЗЬ', callback_data='key_feedback')
check = InlineKeyboardButton('📃 СЧЁТ', callback_data='key_check')
order = InlineKeyboardButton('📦 ЗАКАЗ', callback_data='key_order')
payment = InlineKeyboardButton('💳 ОПЛАТА', callback_data='key_payment')
refund = InlineKeyboardButton('💸 ВОЗВРАТ', callback_data='key_refund')
old.row(order, check, deliver).row(payment, refund, contact).row(feedback, account)

accounts = InlineKeyboardMarkup(resize_keyboard=True)
create = InlineKeyboardButton('СОЗДАНИЕ', callback_data='btn_create')
delete = InlineKeyboardButton('УДАЛЕНИЕ', callback_data='btn_delete')
edit = InlineKeyboardButton('РЕДАКТИРОВАНИЕ', callback_data='btn_edit')
recover = InlineKeyboardButton('ВОССТАНОВЛЕНИЕ ПАРОЛЯ', callback_data='btn_recover')
switch = InlineKeyboardButton('СМЕНА АККАУНТА', callback_data='btn_switch')
accounts.add(create, delete, edit, recover, switch)

contacts = InlineKeyboardMarkup(resize_keyboard=True)
support = InlineKeyboardButton('ОБРАТИТЬСЯ В ТЕХ.ПОДДЕРЖКУ', callback_data='btn_support')
human = InlineKeyboardButton('СВЯЗАТЬСЯ С ОПЕРАТОРОМ', callback_data='btn_human')
contacts.insert(support)
contacts.add(human)

delivers = InlineKeyboardMarkup(resize_keyboard=True)
options = InlineKeyboardButton('ВАРИАНТЫ', callback_data='btn_options')
period = InlineKeyboardButton('СРОКИ', callback_data='btn_period')
delivers.add(options, period)

feedbacks = InlineKeyboardMarkup(resize_keyboard=True)
complaint = InlineKeyboardButton('ЖАЛОБА', callback_data='btn_complaint')
review = InlineKeyboardButton('ОТЗЫВ', callback_data='btn_review')
feedbacks.add(complaint, review)

checks = InlineKeyboardMarkup(resize_keyboard=True)
get = InlineKeyboardButton('ПОЛУЧИТЬ ЧЕК', callback_data='btn_get')
checks.add(get)

orders = InlineKeyboardMarkup(resize_keyboard=True)
cancel = InlineKeyboardButton('ОТМЕНИТЬ', callback_data='btn_cancel')
place = InlineKeyboardButton('РАЗМЕСТИТЬ ОБЪЯВЛЕНИЕ', callback_data='btn_place')
track = InlineKeyboardButton('ОТСЛЕДИТЬ', callback_data='btn_track0')
orders.insert(place)
orders.add(cancel, track)

payments = InlineKeyboardMarkup(resize_keyboard=True)
method = InlineKeyboardButton('СПОСОБЫ ОПЛАТЫ', callback_data='btn_method')
issue = InlineKeyboardButton('ПРОБЛЕМЫ', callback_data='btn_issue')
payments.add(method, issue)

refunds = InlineKeyboardMarkup(resize_keyboard=True)
policy = InlineKeyboardButton('ПОЛИТИКА ВОЗВРАТА', callback_data='btn_policy')
got = InlineKeyboardButton('ОФОРМИТЬ ВОЗВРАТ', callback_data='btn_got')
track = InlineKeyboardButton('ОТСЛЕДИТЬ', callback_data='btn_track1')
refunds.insert(policy)
refunds.insert(got)
refunds.add(track)
