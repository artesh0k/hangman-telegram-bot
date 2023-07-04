# Library
import asyncio
from aiogram import Bot, Dispatcher, executor
from database_commands import db_start
from config import TOKEN_API
from background import keep_alive


loop = asyncio.new_event_loop()
bot = Bot(TOKEN_API, parse_mode='HTML')
dp = Dispatcher(bot, loop=loop)


# ON START UP!
async def on_start_up(_):
    await db_start()
    print('Бота було успішно запущено! The bot has been successfully started!')


# LAUNCHING THE BOT
if __name__ == "__main__":
    from handlers import dp
    keep_alive()
    executor.start_polling(dp, skip_updates=True, on_startup=on_start_up)
