from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram.types import CallbackQuery, Message

from services.shop_service import (
    get_categories,
    get_products_by_category,
    get_product,
    buy_product
)

router = Router()

@router.message(F.text == "🛍 Каталог")
async def catalog_message_handler(message: Message):
    categories = get_categories()

    if not categories:
        await message.answer(
            "📂 Каталог пока пуст.",
            reply_markup=get_back_to_menu_keyboard()
        )
        return

    builder = InlineKeyboardBuilder()

    for category in categories:
        builder.button(
            text=category,
            callback_data=f"category:{category}"
        )

    builder.button(text="🏠 В меню", callback_data="main_menu")
    builder.adjust(1)

    await message.answer(
        "📂 <b>Каталог</b>\n\nВыберите категорию:",
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data == "catalog")
async def catalog_handler(callback: CallbackQuery):
    categories = get_categories()

    if not categories:
        await callback.message.edit_text(
            "📂 Каталог пока пуст.",
            reply_markup=get_back_to_menu_keyboard()
        )
        await callback.answer()
        return

    builder = InlineKeyboardBuilder()

    for category in categories:
        builder.button(
            text=category,
            callback_data=f"category:{category}"
        )

    builder.button(text="🏠 В меню", callback_data="main_menu")
    builder.adjust(1)

    await callback.message.edit_text(
        "📂 <b>Каталог</b>\n\nВыберите категорию:",
        reply_markup=builder.as_markup()
    )

    await callback.answer()


@router.callback_query(F.data.startswith("category:"))
async def category_handler(callback: CallbackQuery):
    category = callback.data.split(":", 1)[1]
    products = get_products_by_category(category)

    if not products:
        await callback.message.edit_text(
            f"📂 <b>{category}</b>\n\n"
            f"В этой категории пока нет товаров.",
            reply_markup=get_catalog_back_keyboard()
        )
        await callback.answer()
        return

    builder = InlineKeyboardBuilder()

    for product in products:
        delivery_type = product.get("delivery_type", "static")

        if delivery_type == "dynamic":
            stock = len(product.get("content", []))
            button_text = f"{product['name']} — {product['price']} ₽ | Остаток: {stock}"
        else:
            button_text = f"{product['name']} — {product['price']} ₽"

        builder.button(
            text=button_text,
            callback_data=f"product:{product['id']}"
        )

    builder.button(text="🔙 Назад", callback_data="catalog")
    builder.button(text="🏠 В меню", callback_data="main_menu")
    builder.adjust(1)

    await callback.message.edit_text(
        f"📂 <b>{category}</b>\n\nВыберите товар:",
        reply_markup=builder.as_markup()
    )

    await callback.answer()


@router.callback_query(F.data.startswith("product:"))
async def product_handler(callback: CallbackQuery):
    product_id = callback.data.split(":", 1)[1]
    product = get_product(product_id)

    if not product:
        await callback.answer("Товар не найден", show_alert=True)
        return

    delivery_type = product.get("delivery_type", "static")

    if delivery_type == "dynamic":
        stock = len(product.get("content", []))
        stock_text = f"\n📦 Остаток: {stock} шт."
    else:
        stock_text = ""

    builder = InlineKeyboardBuilder()

    builder.button(
        text=f"🛒 Купить за {product['price']} ₽",
        callback_data=f"buy:{product['id']}"
    )
    builder.button(
        text="🔙 Назад",
        callback_data=f"category:{product['category']}"
    )
    builder.button(text="🏠 В меню", callback_data="main_menu")
    builder.adjust(1)

    await callback.message.edit_text(
        f"🛍 <b>{product['name']}</b>\n\n"
        f"💰 Цена: {product['price']} ₽"
        f"{stock_text}\n\n"
        f"{product['description']}",
        reply_markup=builder.as_markup()
    )

    await callback.answer()


@router.callback_query(F.data.startswith("buy:"))
async def buy_handler(callback: CallbackQuery):
    product_id = callback.data.split(":", 1)[1]

    success, result = buy_product(callback.from_user.id, product_id)

    if not success:
        await callback.answer(result, show_alert=True)
        return

    product = result

    await callback.message.edit_text(
        f"✅ <b>Покупка успешна!</b>\n\n"
        f"🛍 Товар: {product['name']}\n"
        f"💰 Цена: {product['price']} ₽\n\n"
        f"📦 <b>Выдача:</b>\n"
        f"{product['issued_content']}",
        reply_markup=get_back_to_menu_keyboard()
    )

    await callback.answer("Покупка успешна!")


def get_back_to_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🏠 В меню", callback_data="main_menu")
    return builder.as_markup()


def get_catalog_back_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙 Назад", callback_data="catalog")
    builder.button(text="🏠 В меню", callback_data="main_menu")
    builder.adjust(1)
    return builder.as_markup()