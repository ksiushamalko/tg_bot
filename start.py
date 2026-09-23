from aiogram import Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.reply import ReplyKeyboards
from database.db import Database


def register_start_handlers(dp: Dispatcher):

    @dp.message(Command("start"))
    async def cmd_start(message: Message):
        await Database.add_user(
            user_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
        )
        keyboard = ReplyKeyboards.main_menu()
        await message.answer(
            "Привет!\nЯ твой персональный телеграм-бот.\nЧем могу быть полезен?",
            reply_markup=keyboard,
        )

    @dp.message(Command("crash"))
    async def cmd_crash(message: Message):
        result = 1 / 0
        await message.answer(str(result))

    @dp.message(Command("help"))
    @dp.message(F.text == "Помощь")
    async def cmd_help(message: Message):
        await message.answer(
            "ПОМОЩЬ:\n\n"
            "Доступные команды:\n"
            "1. /start - главное меню\n"
            "2. /photo - показать фото\n"
            "3. /survey - пройти опрос\n"
            "4. /history - моя история\n"
            "5. /stats - статистика\n"
            "6. /clear_history - удалить все мои опросы\n"
            "7. /crash - проверить обработку ошибок\n\n"
            "Используй кнопки внизу для навигации!",
            reply_markup=ReplyKeyboards.main_menu(),
        )

    @dp.message(F.text == "Старт")
    async def handle_start_button(message: Message):
        keyboard = ReplyKeyboards.main_menu()
        await message.answer(
            "Я уже здесь!\nЧем могу быть полезен?",
            reply_markup=keyboard,
        )