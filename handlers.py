# Library
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from main import dp
from hangman import get_word, is_word_guessed, get_guessed_word, get_available_letters
from background import keep_alive
from database_commands import create_profile, create_profile_to_play, get_data, change_count, \
    change_letters_guessed, delete_row, change_language

# user_id->0, secret->1, count->2, letters_guessed->3, language->4
# 🧐✍️✨😭🥰👺😎🙄🛐🤩😂🤧😞❤️🤮😍🌞😩🤪☺️😳🥳😶‍🌫️😡🤝😦😢😉😘😥👸🤨😔🥺😜🤕😄🤔👋☹️😊🇬🇧🇺🇦


kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(KeyboardButton('🇺🇦')).insert(KeyboardButton('🇬🇧'))


# Command: /START
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    # keep_alive()
    id = message.from_user.id
    await message.answer(text="""
Ласкаво просимо до нашого Телеграм Боту.
Welcome to our Telegram bot.
      """)
    await message.answer_animation(animation="CgACAgIAAxkBAAIOX2PEflqP2xcSYF-X1SI0DaXxUSmZAAKPCQACTs5xSImPadHwfWmsLQQ")
    await delete_row(id)
    await create_profile(user_id=message.from_user.id)
    await message.answer(text="Обери мову / Choose language:", reply_markup=kb)


# Command: /HELP
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    keep_alive()
    id = message.from_user.id
    if get_data(id, 2) == 0 and get_data(id, 4) != '':
        if get_data(id, 4) == 'ua':
            await message.answer(text="""
<b>О «Hangman»</b>
Шибениця — це гра, в якій потрібно відгадувати слово по літерах. Вгадані літери відкриваються в загаданому слові, при невдалій спробі малюється наступна частина шибениці. Гра закінчується у випадку, якщо гравець вгадає слово або інший гравець малює цілу шибеницю.

<b>Правила Гри</b>
1. Щоб запустити гру Вам потрібно вести команду /play. 
2. У Вас є 8 спроб, щоб вгадати слово. Віднімається спроба, якщо Ви вводите неправильну літеру, тобто цієї літери нема в наявності задуманого словa, а якщо правильна літера є, то спроби лишаються незмінними. Якщо спроб залишилося - 0, то це значить, що Ви програли.
3. Якщо ввести повністю слово, то гра автоматично видає Вам результат. Ввели одразу правильне слово — перемогли! Ввели неправильне слово — одразу програли! Спроб більше не буде.
4. Якщо Ви повторно вводите літеру, яка вже використовувалась - спроба не знімається.

<b>Команди</b>
/play — почати грати в гру 
/edit_language — змінити мову 

<b>Розробники</b>
Варіч Д. О. — @Dima_Varich
Варіч В. О. — @w0leriy
Рагулін А. О. — @ILAGOTE
Поляков Р. В. — @Catharsy
          """)
        else:
            await message.answer(text="""
<b>About «Hangman»</b>
Hangman is a game in which you have to guess the word by letters. The guessed letters are revealed in the riddled word, with an unsuccessful attempt, the next part of the gallows is drawn. The game ends if a player guesses the word or another player draws the entire gallows.

<b>Game rules</b>
1. To start the game, you need to run the /play command.
2. You have 8 attempts to guess the word. An attempt is subtracted if you enter the wrong letter, that is, this letter is not present in the intended word, and if the correct letter is present, the attempts remain unchanged. If there are 0 attempts left, it means that you have lost.
3. If you enter the word in its entirety, the game will automatically give you the result. They immediately entered the correct word - they won! They entered the wrong word - they immediately lost! There will be no more attempts.
4. If you re-enter a letter that has already been used - the attempt is not removed.

<b>Commands</b>
/play — start playing the game
/edit_language — change language

<b>Creators</b>
Varich D. O. — @Dima_Varich
Varich V. O. - @w0leriy
Ragulin A. O. — @ILAGOTE
Polyakov R. V. — @Catharsy
          """)
    else:
        await message.delete()


@dp.message_handler(commands=['edit_language'])
async def edit_language(message: types.Message):
    # keep_alive()
    id = message.from_user.id
    if get_data(id, 2) == 0:
        await message.answer(text="Обери мову / Choose language:", reply_markup=kb)
        await change_language(id, '')
    else:
        await message.delete()


# Command: /PLAY
@dp.message_handler(commands=['play'])
async def play_command(message: types.Message):
    # keep_alive()
    id = message.from_user.id
    if get_data(id, 2) == 0 and get_data(id, 4) != '':
        await create_profile_to_play(user_id=message.from_user.id, secret=get_word(get_data(id, 4)))
        if get_data(id, 4) == 'gb':
            # await create_profil_to_play(user_id=message.from_user.id, secret=get_word(get_data(id, 4)))
            await message.answer(text=f"🧐 I guessed the word: ||{get_data(id, 1)}||", parse_mode='MarkdownV2')
            await message.answer(text=f"""
Welcome to the game <b>Hangman</b>!
I am thinking of a word that is <b>{len(get_data(id, 1))}</b> letters long
            """)

            print("game was start")

            await message.answer(text=f"""    
------------------------------
You have <b>{get_data(id, 2)}</b> guesses left.
Available letters: {get_available_letters(get_data(id, 3), get_data(id, 4))}
------------------------------
            """)
        else:
            # await create_profil_to_play(user_id=message.from_user.id, secret=get_word(get_data(id, 4)))
            await message.answer(text=f"🧐 Я загадав слово: ||{get_data(id, 1)}||", parse_mode='MarkdownV2')
            await message.answer(text=f"""
Ласкаво просимо до гри <b>Шибениця</b>
Я думаю про слово, яке складається з <b>{len(get_data(id, 1))}</b> літер
                        """)

            print("гра почалась")

            await message.answer(text=f"""    
------------------------------
Ти маєш <b>{get_data(id, 2)}</b> спроб.
Ти можеш використовувати літери: {get_available_letters(get_data(id, 3), get_data(id, 4))}
------------------------------
                        """)
    else:
        await message.delete()


@dp.message_handler(content_types='text')
async def game(message: types.Message):
    # keep_alive()
    id = message.from_user.id

    if get_data(id, 2) != 0:
        if get_data(id, 4) == 'gb':
            alphabet = "qwertyuiopasdfghjklzxcvbnm"
            if len(message.text) == 1 and message.text.lower() in alphabet:
                word = message.text.lower()
                if word in get_data(id, 3):
                    await message.answer(
                        f"Letter ' <b>{word}</b> ' has been used already: {get_guessed_word(get_data(id, 1), get_data(id, 3))}")
                elif word in get_data(id, 1):
                    letters_guessed_new = get_data(id, 3) + word
                    await change_letters_guessed(id, letters_guessed_new)
                    await message.answer(f"Good guess: {get_guessed_word(get_data(id, 1), get_data(id, 3))}")
                    if is_word_guessed(get_data(id, 1), get_data(id, 3)) == 1:
                        await message.answer("🥳 <b>Congratulations, you won!</b>")
                        await message.answer_animation(
                            animation='CgACAgQAAxkBAAIGVWPBlgeuAfUyhDksznKNtkDAtnWZAAK2AgACaYgNU4wtzH86zUCuLQQ')
                        print('id: ', get_data(id, 0), 'won')
                        await change_count(id, 0)
                        return
                else:
                    letters_guessed_new = get_data(id, 3) + word
                    await change_letters_guessed(id, letters_guessed_new)
                    await message.answer(
                        f"Oops! ' <b>{word}</b> ' is not a valid letter: {get_guessed_word(get_data(id, 1), get_data(id, 3))}")

                    await change_count(id, get_data(id, 2) - 1)
                    if get_data(id, 2) == 0:
                        await message.answer(f"😭 Sorry, <b>you lose</b>. The word was <code>{get_data(id, 1)}</code>.")
                        await message.answer_animation(
                            animation='CgACAgQAAxkBAAIGWWPBlk1ToX-nSFX3v65h8fzQgZgAA-QCAAKmWERTuaKDCXVqayItBA')
                        print('id: ', get_data(id, 0), 'lost')
                        await change_count(id, 0)

                        return

                await message.answer(text=f"""
------------------------------
You have <b>{get_data(id, 2)}</b> guesses left.
Available letters: {get_available_letters(get_data(id, 3), get_data(id, 4))}
------------------------------""")
            elif len(message.text) == 1 and message.text not in alphabet:
                await message.answer("Please use only english letters!")
                await message.answer(text=f"""
------------------------------
You have <b>{get_data(id, 2)}</b> guesses left.
Available letters: {get_available_letters(get_data(id, 3), get_data(id, 4))}
word: {get_guessed_word(get_data(id, 1), get_data(id, 3))}
------------------------------""")
            elif len(message.text) > 1:
                if message.text.lower() == get_data(id, 1):
                    await message.answer("🥳 <b>Congratulations, you won!</b>")
                    await message.answer_animation(
                        animation='CgACAgQAAxkBAAIGVWPBlgeuAfUyhDksznKNtkDAtnWZAAK2AgACaYgNU4wtzH86zUCuLQQ')
                    print('id: ', get_data(id, 0), 'won')
                else:
                    await message.answer(f"😭 Sorry, <b>bad guess</b>. The word was <code>{get_data(id, 1)}</code>.")
                    await message.answer_animation(
                        animation='CgACAgQAAxkBAAIGWWPBlk1ToX-nSFX3v65h8fzQgZgAA-QCAAKmWERTuaKDCXVqayItBA')
                    print('id: ', get_data(id, 0), 'lost')
                await change_count(id, 0)
                return
        else:
            alphabet = "'йцукенгґшщзхїфівапролджєячсмитьбю"
            if len(message.text) == 1 and message.text.lower() in alphabet:
                word = message.text.lower()
                if word in get_data(id, 3):
                    await message.answer(
                        f"Літера ' <b>{word}</b> ' вже використовувалась: {get_guessed_word(get_data(id, 1), get_data(id, 3))}")
                elif word in get_data(id, 1):
                    letters_guessed_new = get_data(id, 3) + word
                    await change_letters_guessed(id, letters_guessed_new)
                    await message.answer(f"Гарна спроба: {get_guessed_word(get_data(id, 1), get_data(id, 3))}")
                    if is_word_guessed(get_data(id, 1), get_data(id, 3)) == 1:
                        await message.answer("🥳 <b>Вітання, ти переміг!</b>")
                        await message.answer_animation(
                            animation='CgACAgQAAxkBAAIGVWPBlgeuAfUyhDksznKNtkDAtnWZAAK2AgACaYgNU4wtzH86zUCuLQQ')
                        print('id: ', get_data(id, 0), 'won')
                        await change_count(id, 0)
                        return
                else:
                    letters_guessed_new = get_data(id, 3) + word
                    await change_letters_guessed(id, letters_guessed_new)
                    await message.answer(
                        f"Уупс! ' <b>{word}</b> ' літера не підходить: {get_guessed_word(get_data(id, 1), get_data(id, 3))}")

                    await change_count(id, get_data(id, 2) - 1)
                    if get_data(id, 2) == 0:
                        await message.answer(
                            f"😭 Вибачте, <b>ви програли</b>. Я загадав <code>{get_data(id, 1)}</code>.")
                        await message.answer_animation(
                            animation='CgACAgQAAxkBAAIGWWPBlk1ToX-nSFX3v65h8fzQgZgAA-QCAAKmWERTuaKDCXVqayItBA')
                        print('id: ', get_data(id, 0), 'lost')
                        await change_count(id, 0)

                        return

                await message.answer(text=f"""
------------------------------
Ти маєш <b>{get_data(id, 2)}</b> спроб.
Ти можеш використовувати літери: {get_available_letters(get_data(id, 3), get_data(id, 4))}
------------------------------""")
            elif len(message.text) == 1 and message.text not in alphabet:
                await message.answer("Будь ласка, використовуй тільки українські літери!")
                await message.answer(text=f"""
------------------------------
Ти маєш <b>{get_data(id, 2)}</b> спроб.
Ти можеш використовувати літери: {get_available_letters(get_data(id, 3), get_data(id, 4))}
слово: {get_guessed_word(get_data(id, 1), get_data(id, 3))}
------------------------------"""
                                     )
            elif len(message.text) > 1:
                if message.text.lower() == get_data(id, 1):
                    await message.answer("🥳 <b>Вітання, ти переміг!</b>")
                    await message.answer_animation(
                        animation='CgACAgQAAxkBAAIGVWPBlgeuAfUyhDksznKNtkDAtnWZAAK2AgACaYgNU4wtzH86zUCuLQQ')
                    print('id: ', get_data(id, 0), 'won')
                else:
                    await message.answer(f"😭 Вибачте, <b>ви програли</b>. Я загадав <code>{get_data(id, 1)}</code>.")
                    await message.answer_animation(
                        animation='CgACAgQAAxkBAAIGWWPBlk1ToX-nSFX3v65h8fzQgZgAA-QCAAKmWERTuaKDCXVqayItBA')
                    print('id: ', get_data(id, 0), 'lost')
                await change_count(id, 0)
                return
    else:
        if get_data(id, 4) == '':
            if message.text == '🇬🇧':
                await change_language(id, 'gb')
                await message.answer("Language has been chosen: 🇬🇧", reply_markup=ReplyKeyboardRemove())
                await message.answer_animation(
                    animation="CgACAgQAAxkBAAIMX2PEaxuSXHx370MYiZThZGUs9sRcAALdAgACSHMNU-y3XeWcD72ILQQ")
                await message.answer("Use /play to start the game")

            elif message.text == '🇺🇦':
                await change_language(id, 'ua')
                await message.answer("Мова обрана: 🇺🇦", reply_markup=ReplyKeyboardRemove())
                await message.answer_animation(
                    animation="CgACAgQAAxkBAAIMXGPEaqThQRkHtXYnB7MDS8tEq5JwAAInAwACt3cFU7KZqW-eAAH4Jy0E")
                await message.answer("Щоб почати гру введіть команду /play")

        await message.delete()

    print('id: ', get_data(id, 0), 'count: ', get_data(id, 2))
