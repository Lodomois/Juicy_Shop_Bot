from aiogram.utils.keyboard import InlineKeyboardBuilder


def other_menu():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Политика конфиденциальности",
        callback_data="privacy_policy"
    )

    builder.button(
        text="Пользовательское соглашение",
        callback_data="user_agreement"
    )

    builder.button(text="🏠 В меню", callback_data="main_menu")

    builder.adjust(1)

    return builder.as_markup()


def other_document_menu():
    builder = InlineKeyboardBuilder()

    builder.button(text="🔙 Назад", callback_data="other")
    builder.button(text="🏠 В меню", callback_data="main_menu")

    builder.adjust(1)

    return builder.as_markup()
