from aiogram import Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from keyboards.reply import ReplyKeyboards
from keyboards.inline import InlineKeyboards
# from hendlers.survey import cmd_survey


def register_inline_handlers(dp: Dispatcher):

    @dp.message(Command("menu"))
    async def cmd_menu(message: Message):

        keyboard = InlineKeyboards.main_menu()

        await message.answer(
            "---------- Меню бота ----------\n"
            "Выбери действие:",
            reply_markup=keyboard
        )

    @dp.callback_query()
    async def hendle_callback(callback: CallbackQuery, state: FSMContext):

        await callback.answer()

        data = callback.data

        if data == "info":
            await callback.message.edit_text(
                "Информация о боте: \n"
                "Это мой тестовый бот на aiogram3\n"
                "Он умеет:\n"
                "1. Отвечать на команды\n"
                "2. Отправлять фото\n"
                "3. Проводить опросы\n"
                "4. Работать с клавиатурами\n"
            )
        elif data == "survey":
            
            from hendlers.survey import SurveyStates
            from aiogram.types import ReplyKeyboardRemove

            await callback.message.delete()

            await callback.message.answer(
                        "Опрос запущен...\n"
                        "Как тебя зовут?\n",
                        reply_markup=ReplyKeyboardRemove()
                    )
            await state.set_state(SurveyStates.name)

        elif data == "photo":

            await callback.message.delete()
            await callback.message.answer("Фото отправляется...")

            photo = FSInputFile("core/img/1.jpg")
            await callback.message.answer_photo(
                photo=photo,
                caption="Вот ваш Николас Кейдж!"
            )

        elif data == "close":

            await callback.message.delete()
            await callback.message.answer("Меню закрыто...", reply_markup=ReplyKeyboards.main_menu())