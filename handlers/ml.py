from start_bot import dp
from aiogram import types, Dispatcher
from states.state import *
from keyboards import kb

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


@dp.message_handler(state=LoginUser.state_)
async def ml(message: types.Message):
    request = message.text
    try:
        res = model.predict(tfidfconverter.transform(
            [' '.join([morph.parse(word)[0][2] for word in tokenizer.tokenize(f'{request}')])]).toarray())
        await message.answer(res[0], reply_markup=kb.bot_pomog)
    except Exception as ex_:
        print(ex_)


def register_handlers_ml(dp: Dispatcher):
    dp.register_message_handler(ml)