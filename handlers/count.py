from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
def register_count_handlers(dp: Dispatcher):
    @dp.message(Command("count"))
    async def cmd_count(message: Message, user_count: int):
        await message.answer(f"Вы обратились к боту {user_count} раз(а).")