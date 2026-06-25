from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="🛍 Каталог",
        callback_data="catalog"
    )

    builder.button(
        text="👤 Профиль",
        callback_data="profile"
    )

    builder.button(
        text="⚙️ Прочее",
        callback_data="other"
    )

    builder.adjust(1)

    return builder.as_markup()