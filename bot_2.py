import asyncio
import os
from aiogram import Bot, Dispatcher, types
from dotenv import find_dotenv, load_dotenv 
from database.engine import start

load_dotenv(find_dotenv())

from handlers.user_private import ro    
from common.bot_cmds_list import private
from handlers.admin_private import admin_ro


bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()

dp.include_router(ro)
dp.include_router(admin_ro)





async def main():
    await start()
    await bot.delete_webhook(drop_pending_updates = True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)

asyncio.run(main())