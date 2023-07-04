import sqlite3 as sq


async def db_start():
    global db, cur
    db = sq.connect('new.db')
    cur = db.cursor()
    #cur.execute("DROP TABLE IF EXISTS profile")
    cur.execute("CREATE TABLE IF NOT EXISTS profile(user_id TEXT PRIMARY KEY, secret TEXT, count INTEGER, letters_guessed TEXT, language TEXT)")
    db.commit()


async def create_profile(user_id):
    user = cur.execute("SELECT 1 FROM profile WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO profile VALUES(?, ?, ?, ?, ?)", (user_id, '', 0, '', ''))
    db.commit()


async def create_profile_to_play(user_id, secret):
    cur.execute("UPDATE profile SET secret = '{}', count = '{}', letters_guessed = '{}' WHERE user_id == '{}'".format(
            secret, 8, '', user_id
        ))
    db.commit()


def get_data(user_id, index):
    lol = cur.execute("SELECT user_id, secret, count, letters_guessed, language FROM profile WHERE user_id == '{key}'".format(key=user_id)).fetchall()
    print(lol)
    return lol[0][index]


async def change_count(user_id, count):
    cur.execute("UPDATE profile SET count = '{}' WHERE user_id == '{}'".format(count, user_id))
    db.commit()


async def change_letters_guessed(user_id, letters_guessed):
    cur.execute("UPDATE profile SET letters_guessed = '{}' WHERE user_id == '{}'".format(letters_guessed, user_id))
    db.commit()


async def change_language(user_id, language):
    cur.execute("UPDATE profile SET language = '{}' WHERE user_id == '{}'".format(language, user_id))
    db.commit()


async def delete_row(user_id):
    cur.execute("DELETE FROM profile WHERE user_id='{}'".format(user_id))
    db.commit()
