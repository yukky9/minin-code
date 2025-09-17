from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def cancel_kb():
    kb = [
        [KeyboardButton(text="Отмена")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard
