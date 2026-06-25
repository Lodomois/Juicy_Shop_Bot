from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def reply_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛍 Каталог")],
            [KeyboardButton(text="👤 Профиль")],
            [KeyboardButton(text="⚙️ Прочее")]
        ],
        resize_keyboard=True
    )