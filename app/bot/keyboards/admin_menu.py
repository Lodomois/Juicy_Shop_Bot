from aiogram.utils.keyboard import InlineKeyboardBuilder

def admin_menu():
    builder = InlineKeyboardBuilder()

    builder.button(text="➕ Добавить товар", callback_data="admin_add_product")
    builder.button(text="📦 Список товаров", callback_data="admin_products")
    builder.button(text="🗑 Удалить товар", callback_data="admin_delete_product")
    builder.button(text="💰 Пополнить баланс", callback_data="admin_add_balance")
    builder.button(text="➖ Списать баланс", callback_data="admin_remove_balance")
    builder.button(text="🎁 Добавить промокод", callback_data="admin_add_promo")
    builder.button(text="🏠 В меню", callback_data="main_menu")

    builder.adjust(1)

    return builder.as_markup()


def product_type_menu():
    builder = InlineKeyboardBuilder()

    builder.button(text="📌 Статичный товар", callback_data="product_type_static")
    builder.button(text="🔁 Сменяемый сверху вниз", callback_data="product_type_dynamic")
    builder.button(text="❌ Отмена", callback_data="admin_cancel")

    builder.adjust(1)

    return builder.as_markup()