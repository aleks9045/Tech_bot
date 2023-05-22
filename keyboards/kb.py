from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

change = InlineKeyboardMarkup(resize_keyboard=True)
change_button = InlineKeyboardButton('Изменить информацию', callback_data='change')
change.add(change_button)

classes = ReplyKeyboardMarkup(resize_keyboard=True)
all_ = KeyboardButton('/all_week')
one = KeyboardButton('/today')
other = KeyboardButton('/other')
me = KeyboardButton('/me')
classes.row(all_, one)
classes.row(other, me)

other = InlineKeyboardMarkup(resize_keyboard=True)
tests_button = InlineKeyboardButton('❔Тесты❔', callback_data='tests')
tips_button = InlineKeyboardButton('😊Советы😊', callback_data='tips')
other.add(tests_button, tips_button)

more_tip = InlineKeyboardMarkup(resize_keyboard=True)
tips_button2 = InlineKeyboardButton('Ещё совет', callback_data='tips')
more_tip.add(tips_button2)

tests = InlineKeyboardMarkup(resize_keyboard=True)
rus = InlineKeyboardButton('🖊Русский язык', callback_data='rus')
eng = InlineKeyboardButton('🔤Английский язык', callback_data='eng')
math = InlineKeyboardButton('🔢Математика', callback_data='math')
tests.add(rus, eng, math)

ottf = ReplyKeyboardMarkup(resize_keyboard=True)
one = KeyboardButton('1')
two = KeyboardButton('2')
three = KeyboardButton('3')
four = KeyboardButton('4')
ottf.row(one, two)
ottf.add(three, four)