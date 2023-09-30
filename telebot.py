import asyncio
import logging
import sys
from aiogram.fsm.state import StatesGroup, State
import random
from config import TBOT_API
from game import BullsCows, Cities
from keyboard import make_keyboard_games, make_keyboard_lvl

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


levels = ("легкий", "средний", "сложный")
stop = ("stop", "quit", "закончить", "стоп", "выход")
b_names = {0: "быков",
           1: "бык",
           2: "быка",
           3: "быка",
           4: "быка",
           5: "быков"}

c_names = {0: "коров",
           1: "корова",
           2: "коровы",
           3: "коровы",
           4: "коровы",
           5: "коров"}


# Запуск диспетчера
dp = Dispatcher()


class Games(StatesGroup):
    """Состояния для сохранения этапов в диалоге"""
    choosing_game = State()
    bools_cows_level = State()
    bools_cows = State()
    cities_level = State()
    cities = State()


@dp.message(Command('start'))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    """Обработка команды /start"""
    await message.answer(f"Привет, {message.from_user.first_name}!\n"
                         f"В какую игру сыграем?", reply_markup=make_keyboard_games())
    # Установка состояния выбора игры
    await state.set_state(Games.choosing_game)


@dp.message(Games.choosing_game)
async def choose_game(message: Message, state: FSMContext) -> None:
    """Отработка состояния выбор игры"""
    if message.text.lower() == "быки и коровы":
        await state.set_state(Games.bools_cows_level)
        await message.reply("Отличный выбор!")
        await message.answer("Правила игры:\nНеобходимо угадать загаданное число, состоящее из разных цифр. "
                             "Если цифра есть в числе, но стоит не на своем месте - это корова. "
                             "Если цифра стоит на правильном месте - это бык. Для выхода из игры наберите <i>выход</i>."
                             "\nВыберите сложность игры:",
                             reply_markup=make_keyboard_lvl(levels))
    elif message.text.lower() == "города россии":
        await state.set_state(Games.cities_level)
        await message.reply("Отличный выбор!")
        await message.answer("Правила игры:\nНеобходимо называть города России на последнюю "
                             "букву предыдущего города. Для выхода из игры наберите <i>выход</i>."
                             "\nВыберите сложность игры:",
                             reply_markup=make_keyboard_lvl(levels))
    else:
        await state.set_state(Games.choosing_game)
        await message.answer(f"Выберите игру?", reply_markup=make_keyboard_games())


@dp.message(Games.cities_level)
async def choose_cities_level(message: Message, state: FSMContext):
    """Обработка состояния выбор уровня игры города"""
    if message.text.lower() in levels:
        if message.text.lower() == levels[0]:
            city_game = Cities("1")
        elif message.text.lower() == levels[1]:
            city_game = Cities("2")
        elif message.text.lower() == levels[2]:
            city_game = Cities("3")
        await state.update_data(cities=city_game)
        await state.set_state(Games.cities)
        await message.answer(text=f"Введите название города России на букву {city_game.last_char.upper()}",
                             reply_markup=types.ReplyKeyboardRemove())
    elif message.text == "<  К выбору игры":
        await state.set_state(Games.choosing_game)
        await message.answer(text="Выберите игру",
                             reply_markup=make_keyboard_games())
    else:
        await state.set_state(Games.cities_level)
        await message.answer("Выберите сложность игры:",
                             reply_markup=make_keyboard_lvl(levels))


@dp.message(Games.bools_cows_level)
async def choose_bulls_cows_level(message: Message, state: FSMContext):
    """Обработка состояния выбор уровня игры быки и коровы"""
    if message.text.lower() in levels:
        if message.text.lower() == levels[0]:
            n = "3"
        elif message.text.lower() == levels[1]:
            n = "4"
        elif message.text.lower() == levels[2]:
            n = "5"
        await state.update_data(bc=BullsCows(n))
        await state.set_state(Games.bools_cows)
        await message.answer(text=f"Введите {n}-значное число",
                             reply_markup=types.ReplyKeyboardRemove())
    elif message.text == "<  К выбору игры":
        await state.set_state(Games.choosing_game)
        await message.answer(text="Выберите игру",
                             reply_markup=make_keyboard_games())
    else:
        await state.set_state(Games.bools_cows_level)
        await message.answer("Выберите сложность игры:",
                             reply_markup=make_keyboard_lvl(levels))


@dp.message(Games.cities)
async def run_game_cities(message: Message, state: FSMContext):
    data = await state.get_data()
    city = data['cities']
    check = city.check_city(message.text)
    if check[0]:
        city_last_char = city.get_last_char(message.text)
        next_city = city.random_city(city_last_char)
        next_city_last_char = city.get_last_char(next_city).upper()
        if next_city:
            await message.answer(random.choice(["😀", "😜", "🤗", "🔥", "🥳", "🎊"]))
            await message.answer(f"{check[1]}\n\n{next_city}\n"
                                 f"Назовите город на букву "
                                 f"<b>{next_city_last_char}</b>")
        else:
            await state.set_state(Games.cities_level)
            await message.answer("💝")
            await message.answer(f"Поздравляю 🎉, вы победили!",
                                 reply_markup=make_keyboard_lvl(levels))
    else:
        if message.text.lower() in stop:
            await exit_game(message, state)
        else:
            await message.answer("😏")
            await message.answer(f"{check[1]}\nПопробуйте еще раз")


@dp.message(Games.bools_cows)
async def run_game_bulls_cows(message: Message, state: FSMContext):
    """"""
    # Получаем экземпляр класса из хранилища данных
    data = await state.get_data()
    bc = data['bc']
    # Проверка введенного числа на корректность
    check = bc.check_number(message.text)
    if check[0]:
        b, c = bc.check_bulls_cows(message.text)
        await message.answer(f"{b} - {b_names[b]} {b * '🦄'}, {c} - {c_names[c]} {c * '🐮'}")
        if b == 0 and c == 0:
            await message.answer("💩")

        # Конец игры, когда все быки угаданы
        if b == bc.num_digits:
            # Возврат в состояние выбора уровня игры
            await state.set_state(Games.bools_cows_level)
            await message.answer("💝")
            await message.answer(f"Поздравляю 🎉, вы угадали число за {bc.attempts} попыток!",
                                 reply_markup=make_keyboard_lvl(levels))
    # Если число некорректно, выводится сообщение о соответствующей ошибке
    else:
        if message.text.lower() in stop:
            await exit_game(message, state)
        else:
            await message.answer(text=check[1])


async def exit_game(message: Message, state: FSMContext):
    await state.set_state(Games.choosing_game)
    await message.answer("😔")
    await message.answer(f"{message.from_user.first_name}, очень жаль, "
                         f"что вы не хотите больше играть. Жду вас снова.",
                         reply_markup=make_keyboard_games())


@dp.message()
async def begin(message: Message):
    """Отработка произвольных сообщений вначале"""
    await message.answer("для начала наберите /start")


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TBOT_API, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
