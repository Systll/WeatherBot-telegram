from aiogram import Bot, Dispatcher
from handlers import router
import aiogram
import asyncio
import logging


with open('data/bot_token.txt', 'r') as file:
    token = file.read().strip()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)
dp = Dispatcher()


async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
