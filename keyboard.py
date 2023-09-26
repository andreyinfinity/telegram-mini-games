from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def make_keyboard_games():
    kb = [[KeyboardButton(text="Быки и коровы")]]
    return ReplyKeyboardMarkup(keyboard=kb,
                               resize_keyboard=True,
                               input_field_placeholder="Выберите игру:")


def make_keyboard_bc_lvl(levels: tuple):
    kb = [KeyboardButton(text=item) for item in levels]
    return ReplyKeyboardMarkup(keyboard=[kb],
                               resize_keyboard=True,
                               input_field_placeholder="Выберите сложность игры:")
