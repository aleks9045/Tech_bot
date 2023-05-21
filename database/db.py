import aiosqlite
from Data import config


async def add_operator(chat_id):
    async with aiosqlite.connect(r'database/users_id.db') as db:
        await db.execute(f"""INSERT INTO operators (id) VALUES({chat_id})""")
        await db.commit()


async def del_operator(chat_id):
    async with aiosqlite.connect(r'database/users_id.db') as db:
        await db.execute(f"""DELETE FROM operators WHERE id = {chat_id}""")
        await db.commit()


async def get_all_operators():
    async with aiosqlite.connect(r'database/users_id.db') as db:
        res = await db.execute(f"""SELECT id FROM operators""")
        res = await res.fetchall()
        return res


async def new_user(id_, class_, name):
    async with aiosqlite.connect(r'database/users_id.db') as db:
        await db.execute(f"""INSERT INTO users (id, class, name) VALUES({id_}, "{class_}", "{name}")""")
        await db.commit()


async def get_all_users_id():
    async with aiosqlite.connect(r'database/users_id.db') as db:
        result = []
        res = await db.execute(f"""SELECT id FROM users""")
        res = await res.fetchall()
        for i in res:
            result.append(i[0])
        return result


async def get_all_users_info(id_):
    async with aiosqlite.connect(r'database/users_id.db') as db:
        res = await db.execute(f"""SELECT * FROM users WHERE id={id_}""")
        res = await res.fetchall()
        return res


async def change_user_info(class_, name_, id_):
    async with aiosqlite.connect(r'database/users_id.db') as db:
        await db.execute(f"""UPDATE users set class = "{class_}", name = "{name_}" WHERE id = {id_}""")
        await db.commit()


async def get_week_shedule():
    async with aiosqlite.connect(r'database/users_id.db') as db:
        res = await db.execute(f'''SELECT * FROM shedule''')
        res = await res.fetchall()
        return res


async def get_task():
    async with aiosqlite.connect(r'database/users_id.db') as db:
        res = await db.execute(f'''SELECT * FROM tasks''')
        res = await res.fetchall()
        return res


async def get_answer():
    async with aiosqlite.connect(r'database/users_id.db') as db:
        res = await db.execute(f'''SELECT * FROM answers''')
        res = await res.fetchall()
        return res


async def get_tip():
    async with aiosqlite.connect(r'database/users_id.db') as db:
        res = await db.execute(f'''SELECT * FROM tips''')
        res = await res.fetchall()
        return res