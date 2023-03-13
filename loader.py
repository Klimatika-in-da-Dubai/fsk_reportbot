import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage

from src.models import User

import config

import logging

logging.basicConfig(
    format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %H:%M:%S", level=logging.INFO
)


users: dict[int, User] = {}

bot = Bot(token=config.TELEGRAM_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


def on_startup():
    from src.handlers import handlers_router

    dp.include_router(handlers_router)


async def main():
    on_startup()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
