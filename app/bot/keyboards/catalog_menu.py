from aiogram.utils.keyboard import InlineKeyboardBuilder


def catalog_menu():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="📁 Brawl Stars",
        callback_data="cat_brawl"
    )

    builder.button(
        text="💎 ИИ Подписки",
        callback_data="cat_ai"
    )

    builder.button(
        text="🟨 Social Club",
        callback_data="cat_sc"
    )

    builder.button(
        text="🎮 Автореги Steam",
        callback_data="cat_steam"
    )

    builder.button(
        text="⬛ Донат Supercell",
        callback_data="cat_supercell"
    )

    builder.button(
        text="🕹 Боты",
        callback_data="cat_bots"
    )

    builder.button(
        text="🏠 Меню",
        callback_data="main_menu"
    )

    builder.adjust(1)

    return builder.as_markup()