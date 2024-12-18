#main.py

import asyncio
from aiogram import Dispatcher, Bot, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from app.handlers import router #импортируем роутер из hendlers для передачи запросов
from app.handlers import * 
from app.commands import *
import app.keyboard as kb


#главная функция которая запускает проект
async def main():
    dp = Dispatcher()# сам диспетчер
    dp.include_router(router)#здесь передаём диспетчеру запросы из папки handlers благодоря роутеру
    await bot.send_message(admin_id, "Bot is runnig", reply_markup=kb.main) 
    try:
        asyncio.create_task(lock_check())
        await dp.start_polling(bot)  # Стартуем polling
    finally:
        await bot.session.close()  # Корректно закрываем сессию
   

  
if __name__ == "__main__":
    try:
        print('Боже да хоть чтото блять')
        asyncio.run(main())#запускаем главную функцию
    except (KeyboardInterrupt, SystemExit):
        print('Бот выключен')