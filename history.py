from aiogram import Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from database.db import Database
from keyboards.inline import InlineKeyboards

PAGE_SIZE = 3


def register_history_handlers(dp: Dispatcher):

    @dp.message(Command("history"))
    async def cmd_history(message: Message):
        user_id = message.from_user.id
        surveys = await Database.get_user_surveys(user_id)

        if not surveys:
            await message.answer(
                "У тебя нет опросов!\n"
                "Пройди опрос: /survey"
            )
            return

        total_pages = (len(surveys) + PAGE_SIZE - 1) // PAGE_SIZE

        await show_page(message, surveys, page=0, total_pages=total_pages, edit=False)

    async def show_page(message, surveys, page: int, total_pages: int, edit: bool = False):
        start = page * PAGE_SIZE
        end = start + PAGE_SIZE
        page_items = surveys[start:end]

        text = f"История опросов (стр. {page + 1}/{total_pages}):\n\n"

        for i, survey in enumerate(page_items, start=start+1):
            name, age, city, language, created_at = survey
            text += (
                f"{i}. {created_at}\n"
                f"{name}, {age} лет, {city}\n"
                f"Язык программирования: {language}\n\n"
            )

        keyboard = InlineKeyboards.pagination(page, total_pages)

        if edit:
            try:
                await message.edit_text(text, reply_markup=keyboard)
            except Exception:
                await message.answer(text, reply_markup=keyboard)
        else:
            await message.answer(text, reply_markup=keyboard)

    @dp.callback_query(F.data.startswith("page_"))
    async def handle_pagination(callback: CallbackQuery):
        page = int(callback.data.split("_")[1])
        user_id = callback.from_user.id
        surveys = await Database.get_user_surveys(user_id)
        total_pages = (len(surveys) + PAGE_SIZE - 1) // PAGE_SIZE

        await show_page(callback.message, surveys, page, total_pages, edit=True)
        await callback.answer()

   