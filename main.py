import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile

from config import BotConfig
from handlers import register_all_handlers

from middlewares.logging_middleware import LoggingMiddleWare
from middlewares.auth import AdminMiddleware
from middlewares.error_middleware import ErrorsMidleware

from database.db import Database


class TelegramBot:

    def __init__(self):

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[
                logging.FileHandler("bot.log", encoding="utf-8"),
                logging.StreamHandler(),
            ],
        )

        self.token = BotConfig.get_token()
        self.bot = Bot(token=self.token)
        self.dp = Dispatcher()

        self._setup_middlewares()
        register_all_handlers(self.dp)

        logging.info("бот инициализирован...")

    def _setup_middlewares(self):
        self.dp.update.outer_middleware(LoggingMiddleWare())
        self.dp.update.outer_middleware(ErrorsMidleware(1141760956))

    async def start(self):
        await Database.init()
        bot_info = await self.bot.me()
        logging.info(
            "Бот запущен! Имя: %s, username: %s, id: %s",
            bot_info.first_name,
            bot_info.username,
            bot_info.id,
        )
        await self.dp.start_polling(self.bot, skip_updates=True)


async def main():
    bot = TelegramBot()
    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())