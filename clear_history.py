from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from database.db import Database


def register_clear_history_handlers(dp: Dispatcher):

    @dp.message(Command("clear_history"))
    async def cmd_clear_history(message: Message):
        user_id = message.from_user.id

        try:
            count = await Database.count_surveys_user(user_id)

            if count == 0:
                await message.answer("У тебя нет опросов для удаления")
                return

            deleted = await Database.delete_user_surveys(user_id)
            await message.answer(f"Все опросы удалены ({deleted} шт.)")

        except Exception as e:
            print(f"Ошибка при удалении опросов пользователя {user_id}: {e}")
            await message.answer("Не удалось удалить опросы, попробуй позже")