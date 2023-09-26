import asyncio
import logging
import sys
from aiogram.fsm.state import StatesGroup, State

from config import TBOT_API
from game import BullsCows
from keyboard import make_keyboard_games, make_keyboard_bc_lvl

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


bc_levels = ("легкий", "средний", "сложный")

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


@dp.message(Command('start'))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    """
    Обработка сообщения с командой /start
    """
    await message.answer(f"Привет, {message.from_user.first_name}!\n"
                         f"В какую игру сыграем?", reply_markup=make_keyboard_games())
    # Установка состояния выбора игры
    await state.set_state(Games.choosing_game)


@dp.message(Games.choosing_game, F.text.lower() == "быки и коровы")
async def choose_level_bulls_cows(message: Message, state: FSMContext):
    """Фильтр на текст быки и коровы при условии, что состояние choosing_game.
    В других состояниях фильтр не обрабатывается."""
    await message.reply("Отличный выбор!", reply_markup=types.ReplyKeyboardRemove())
    await message.answer("Правила игры:\nНеобходимо угадать загаданное число, состоящее из разных цифр. "
                         "Если цифра есть в числе, но стоит не на своем месте - это корова. "
                         "Если цифра стоит на правильном месте - это бык. Выбери сложность игры:",
                         reply_markup=make_keyboard_bc_lvl(bc_levels))
    # Установка состояния выбора сложности
    await state.set_state(Games.bools_cows_level)


@dp.message(Games.bools_cows_level, F.text.in_(bc_levels))
async def run_bulls_cows(message: Message, state: FSMContext):
    """Фильтр на состояние выбор уровня сложности и текста легкая"""
    if message.text.lower() == bc_levels[0]:
        # Создание экземпляра класса BullsCows и запись его в хранилище данных по ключу easy
        await state.update_data(bc=BullsCows("3"))
        # Установка состояния bools_cows_easy
        await state.set_state(Games.bools_cows)
        await message.answer(text="Введите 3-значное число",
                             reply_markup=types.ReplyKeyboardRemove())
    elif message.text.lower() == bc_levels[1]:
        await state.update_data(bc=BullsCows("4"))
        await state.set_state(Games.bools_cows)
        await message.answer(text="Введите 4-значное число",
                             reply_markup=types.ReplyKeyboardRemove())
    else:
        await state.update_data(bc=BullsCows("5"))
        await state.set_state(Games.bools_cows)
        await message.answer(text="Введите 5-значное число",
                             reply_markup=types.ReplyKeyboardRemove())


@dp.message(Games.bools_cows)
async def check_number(message: Message, state: FSMContext):
    """Фильтр на состояние легкий уровень сложности"""
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
                                 reply_markup=make_keyboard_bc_lvl(bc_levels))
    # Если число некорректно, выводится сообщение о соответствующей ошибке
    else:
        await message.answer(text=check[1])


@dp.message(Games.bools_cows_level)
async def bull_cows_incorrect_level(message: Message):
    """Отработка неверно введенного уровня сложности"""
    await message.answer(text="непонятный уровень сложности",
                         reply_markup=make_keyboard_bc_lvl(bc_levels))


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
