import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from config import BOT_TOKEN
from database import init_db
from handlers import router


async def main():
    logging.basicConfig(level=logging.INFO)
    await init_db()
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    # Clean command menu: keep only /start (removes any old /faq command)
    await bot.delete_my_commands()
    await bot.set_my_commands([BotCommand(command="start", description="Start / restart")])
    await bot.delete_webhook(drop_pending_updates=True)
    logging.info("Bot started. Polling…")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
