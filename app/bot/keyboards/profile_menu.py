from aiogram.utils.keyboard import InlineKeyboardBuilder


def profile_menu():
    builder = InlineKeyboardBuilder()

    builder.button(text="💳 Пополнить баланс", callback_data="deposit")
    builder.button(text="📦 Мои покупки", callback_data="purchases")
    builder.button(text="🎁 Промокод", callback_data="promo")
    builder.button(text="🌐 Язык", callback_data="language")
    builder.button(text="🏠 В меню", callback_data="main_menu")

    builder.adjust(1)

    return builder.as_markup()