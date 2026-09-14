from aiogram import Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.reply import ReplyKeyboards

def register_start_handlers(dp: Dispatcher):

    @dp.message(Command("start"))
    async def cmd_start(message: Message):

        keyboard = ReplyKeyboards.main_menu() #? Вызов метода для создания главного окна меню

        await message.answer(
            "Привет!\nЯ твой персональный телеграм-бот.\nЧем могу быть полезен?",
            reply_markup=keyboard
        )

    
    @dp.message(F.text == "Старт")
    async def handle_start_button(message: Message):

        keyboard = ReplyKeyboards.main_menu() #? Вызов метода для создания главного окна меню

        await message.answer(
            "Я уже здесь!\nЧем могу быть полезен?",
            reply_markup=keyboard
        )

    @dp.message(F.text == "Помощь")
    async def handle_help_button(message: Message):

        await message.answer(
            "ПОМОЩЬ:"
            "Доступные команды: "
            "1. /start - главное меню"
            "2. /photo - показать фото"
            "3. /help - справочный материал"
            "Используй кнопки внизу для навигации!"
        )