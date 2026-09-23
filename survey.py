from aiogram import Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.reply import ReplyKeyboards
from database.db import Database


class SurveyStates(StatesGroup):  #? Определение состояния опроса

    name = State()
    age = State()
    city = State()
    language = State()


def register_survey_handlerds(dp: Dispatcher):  #? регистрация обработчиков

    @dp.message(Command("survey"))  #? Команда для запуска опроса
    async def cmd_survey(message: Message, state: FSMContext):

        await message.answer(
            "Опрос запущен...\n"
            "Как тебя зовут?\n",
            reply_markup=ReplyKeyboardRemove()
        )

        await state.set_state(SurveyStates.name)

    @dp.message(Command("ping"))
    async def cmd_ping(message: Message):
        await message.answer("pong")

    @dp.message(SurveyStates.name)
    async def process_name(message: Message, state: FSMContext):  #? Обработчик состояния имени

        await state.update_data(name=message.text)

        await state.set_state(SurveyStates.age)
        await message.answer("Сколько тебе лет?")

    @dp.message(SurveyStates.age)
    async def process_age(message: Message, state: FSMContext):

        if not message.text.isdigit():
            await message.answer("Ошибка. Введите число...")
            return

        await state.update_data(age=int(message.text))

        await state.set_state(SurveyStates.city)
        await message.answer("В каком городе ты живешь?")

    @dp.message(SurveyStates.city)
    async def process_city(message: Message, state: FSMContext):

        await state.update_data(city=message.text)

        await state.set_state(SurveyStates.language)
        await message.answer("Какой твой любимый язык программирования?")

    @dp.message(SurveyStates.language)
    async def process_language(message: Message, state: FSMContext):

        await state.update_data(language=message.text)

        data = await state.get_data()  #? Получение всех данных

        #? Сохранение опроса в базу данных
        await Database.save_survey(
            user_id=message.from_user.id,
            name=data.get("name"),
            age=data.get("age"),
            city=data.get("city"),
            language=data.get("language"),
        )

        result_text = (
            "Опрос пройден!\n"
            f"Имя: {data.get('name')}\n"
            f"Возраст: {data.get('age')}\n"
            f"Город: {data.get('city')}\n"
            f"Язык программирования: {data.get('language')}\n\n"
            "Спасибо за участие!"
        )

        keyboard = ReplyKeyboards.main_menu()
        await message.answer(result_text, reply_markup=keyboard)

        await state.clear()  #? Очищаем состояние

    @dp.message(Command("cancel"))
    async def cmd_cancel(message: Message, state: FSMContext):

        current_state = await state.get_state()

        if current_state is None:
            await message.answer(
                "У нас нет активных диалогов!...",
                reply_markup=ReplyKeyboards.main_menu()
            )
            return

        await state.clear()
        await message.answer("Диалог отменен...", reply_markup=ReplyKeyboards.main_menu())