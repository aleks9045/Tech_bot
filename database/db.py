import aiosqlite
from Data import config


async def add_queue(chat_id):
    """Добавляем chat_id пользователя в БД"""
    if chat_id in config.operators:
        async with aiosqlite.connect(r'database/users_id.db') as db:
            await db.execute(f"""UPDATE queue_operator set busy = 1 WHERE operator_id = {chat_id}""")
            await db.commit()
    else:
        async with aiosqlite.connect(r'database/users_id.db') as db:
            await db.execute(f"""INSERT INTO queue_user (user_id) VAlUES({chat_id})""")
            await db.commit()


async def delete_queue(chat_id):
    """Удаляем chat_id пользователя в БД или делаем оператора не занятым"""
    if chat_id in config.operators:
        async with aiosqlite.connect(r'database/users_id.db') as db:
            await db.execute(f"""UPDATE queue_operator set busy = 0 WHERE operator_id = {chat_id}""")
            await db.commit()
    else:
        async with aiosqlite.connect(r'database/users_id.db') as db:
            await db.execute(f"""DELETE FROM queue_user WHERE user_id = {chat_id}""")
            await db.execute(f"""UPDATE queue_operator set busy = 0 WHERE operator_id = {chat_id}""")
            await db.commit()


async def delete_chat(id_chat):
    """Удаляем chat_id пользователя в БД"""
    async with aiosqlite.connect(r'database/users_id.db') as db:
        await db.execute(f"""DELETE FROM chats WHERE id = {id_chat}""")
        await db.commit()


async def get_chat(chat_id):
    """Проверяем доступный чат"""
    if chat_id in config.operators:
        async with aiosqlite.connect(r'database/users_id.db') as db:
            res = await db.execute(f"""SELECT * FROM queue_user""", ())
            rows = await res.fetchmany(1)
            if bool(len(rows)):
                for row in rows:
                    return row[1]
            else:
                return False
    else:
        async with aiosqlite.connect(r'database/users_id.db') as db:
            res = await db.execute(f"""SELECT * FROM queue_operator""", ())
            rows = await res.fetchall()
            for row in rows:
                if row[2]:
                    return row[1]
            return False


async def get_active_chat(chat_id):
    '''Получение активного чата'''
    async with aiosqlite.connect(r'database/users_id.db') as db:
        chat = await db.execute(f"""SELECT * FROM chats WHERE chat1 = {chat_id}""", ())
        chat = await chat.fetchall()
        chat_info = []
        id_chat = 0
        for row in chat:
            id_chat = row[0]
            chat_info = [row[0], row[1], row[2]]
        if chat_id == 0:
            return False
        else:
            return chat_info


async def check_active_chat(chat_id):
    '''Проверка на чат'''
    async with aiosqlite.connect(r'database/users_id.db') as db:
        chat = await db.execute(f"""SELECT * FROM chats""", ())
        chat = await chat.fetchall()
        if not chat:
            return False
        id_chat = 0
        for row in chat:
            id_chat = row[0]
            chat_info = [row[0], row[1], row[2]]
        if chat_id == 0:
            return False
        else:
            return chat_info


async def create_chat(one, two):
    """Добавляем чат"""
    async with aiosqlite.connect(r'database/users_id.db') as db:
        if two != False:
            # Создание чата
            await db.execute(f"""DELETE FROM queue_user WHERE user_id = {two}""")
            await db.execute(f"""INSERT INTO chats (chat1, chat2) VAlUES({one}, {two})""")
            await db.execute(f"""UPDATE queue_operator set busy = 0 WHERE operator_id = {one}""")
            await db.commit()
            return True
        else:
            # Становимся в очередь
            return False


async def add_operator(chat_id):
    async with aiosqlite.connect(r'database/users_id.db') as db:
        await db.execute(f"""INSERT INTO queue_operator (operator_id) VALUES({chat_id})""")
        await db.commit()


async def del_operator(chat_id):
    async with aiosqlite.connect(r'database/users_id.db') as db:
        await db.execute(f"""DELETE FROM queue_operator WHERE operator_id = {chat_id}""")
        await db.commit()


async def get_all_operators():
    async with aiosqlite.connect(r'database/users_id.db') as db:
        result = []
        res = await db.execute(f"""SELECT operator_id FROM queue_operator""")
        res = await res.fetchall()
        for i in res:
            result.append(i[0])
        return result


async def vi_vishli_iz_chata(chat_id):
    async with aiosqlite.connect(r'database/users_id.db') as db:
        chat = await db.execute(f"""SELECT * FROM chats""")
        chat = await chat.fetchall()
        for row in chat:
            print(row[0], row[1], row[2])
            if row[1] == chat_id:
                return row[2]
            elif row[2] == chat_id:
                return row[1]