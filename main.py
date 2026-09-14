import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BotConfig
from handlers import register_all_handlers
from middlewares.logging_middleware import LoggingMiddleWare
from middlewares.counter import CounterMiddleware
from middlewares.night_mode import NightModeMiddleware
class TelegramBot:

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.token = BotConfig.get_token()
        self.bot = Bot(token=self.token)
        self.dp = Dispatcher()
        self._setup_middlewares()
        register_all_handlers(self.dp)
        logging.info("бот инициализирован...")
    def _setup_middlewares(self):
        self.dp.update.outer_middleware(LoggingMiddleWare())
        self.dp.update.outer_middleware(CounterMiddleware())
        self.dp.update.outer_middleware(NightModeMiddleware(start_hour=23, end_hour=7))
    async def start(self):
        bot_info = await self.bot.me()
        print(
            f"Бот запущен!\n"
            f"Имя бота: {bot_info.first_name}\n"
            f"Username: {bot_info.username}\n"
            f"ID: {bot_info.id}"
        )
        await self.dp.start_polling(self.bot, skip_updates=True)
async def main():
    bot = TelegramBot()
    await bot.start()
if __name__ == "__main__":
    asyncio.run(main())