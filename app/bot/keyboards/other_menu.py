from aiogram.utils.keyboard import InlineKeyboardBuilder


def other_menu():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="📄 Политика конфиденциальности",
        callback_data="legal:privacy:0"
    )
    builder.button(
        text="📑 Пользовательское соглашение",
        callback_data="legal:terms:0"
    )
    builder.button(text="🏠 В меню", callback_data="main_menu")

    builder.adjust(1)

    return builder.as_markup()
