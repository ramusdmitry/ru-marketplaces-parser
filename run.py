import asyncio
import logging
import os
import dotenv
from aiogram import Bot, Dispatcher
from app.handlers import router
from worker.worker import periodic_parsing, periodic_advertising

dotenv.load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(router)
    asyncio.create_task(periodic_parsing(bot, interval=20))
    # asyncio.create_task(periodic_advertising(bot, interval=30))
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
