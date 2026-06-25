from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config.config import ADMIN_ID

from bot.keyboards.admin_menu import admin_menu, product_type_menu
from bot.states.admin_states import AddProduct, ChangeBalance, DeleteProduct, AddPromo
from services.shop_service import (
    add_product,
    load_products,
    add_balance,
    remove_balance,
    delete_product,
    add_promocode
)

router = Router()


def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID


@router.message(Command("admin"))
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Нет доступа.")
        return

    await message.answer(
        "⚙️ <b>Админ-панель</b>\n\nВыберите действие:",
        reply_markup=admin_menu()
    )


@router.callback_query(F.data == "admin_add_product")
async def admin_add_product(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return

    await state.set_state(AddProduct.delivery_type)

    await callback.message.edit_text(
        "➕ <b>Добавление товара</b>\n\n"
        "Выберите тип выдачи товара:",
        reply_markup=product_type_menu()
    )

    await callback.answer()


@router.callback_query(F.data == "product_type_static")
async def product_type_static(callback: CallbackQuery, state: FSMContext):
    await state.update_data(delivery_type="static")
    await state.set_state(AddProduct.category)

    await callback.message.edit_text(
        "📌 <b>Статичный товар</b>\n\n"
        "Введите категорию товара:"
    )

    await callback.answer()


@router.callback_query(F.data == "product_type_dynamic")
async def product_type_dynamic(callback: CallbackQuery, state: FSMContext):
    await state.update_data(delivery_type="dynamic")
    await state.set_state(AddProduct.category)

    await callback.message.edit_text(
        "🔁 <b>Сменяемый товар</b>\n\n"
        "Введите категорию товара:"
    )

    await callback.answer()


@router.callback_query(F.data == "admin_cancel")
async def admin_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.message.edit_text(
        "⚙️ <b>Админ-панель</b>\n\nВыберите действие:",
        reply_markup=admin_menu()
    )

    await callback.answer()


@router.message(AddProduct.category)
async def add_product_category(message: Message, state: FSMContext):
    await state.update_data(category=message.text)
    await state.set_state(AddProduct.name)

    await message.answer("Введите название товара:")


@router.message(AddProduct.name)
async def add_product_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddProduct.price)

    await message.answer("Введите цену товара числом:")


@router.message(AddProduct.price)
async def add_product_price(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❗ Цена должна быть числом. Попробуйте ещё раз:")
        return

    await state.update_data(price=int(message.text))
    await state.set_state(AddProduct.description)

    await message.answer("Введите описание товара:")


@router.message(AddProduct.description)
async def add_product_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(AddProduct.content)

    await message.answer(
        "Введите выдачу товара.\n\n"
        "Для статичного товара — один текст.\n"
        "Для сменяемого товара — каждая строка отдельная выдача."
    )


@router.message(AddProduct.content)
async def add_product_content(message: Message, state: FSMContext):
    await state.update_data(content=message.text)

    data = await state.get_data()

    product = add_product(
        category=data["category"],
        name=data["name"],
        price=data["price"],
        description=data["description"],
        content=data["content"],
        delivery_type=data["delivery_type"]
    )

    await state.clear()

    await message.answer(
        f"✅ <b>Товар добавлен</b>\n\n"
        f"ID: <code>{product['id']}</code>\n"
        f"Категория: {product['category']}\n"
        f"Название: {product['name']}\n"
        f"Цена: {product['price']} ₽",
        reply_markup=admin_menu()
    )


@router.callback_query(F.data == "admin_products")
async def admin_products(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return

    products = load_products()

    if not products:
        await callback.message.edit_text(
            "📦 Товаров пока нет.",
            reply_markup=admin_menu()
        )
        await callback.answer()
        return

    text = "📦 <b>Список товаров</b>\n\n"

    for product in products:
        status = "✅" if product.get("active") else "❌"
        delivery_type = product.get("delivery_type", "static")

        if delivery_type == "dynamic":
            stock = len(product.get("content", []))
            type_text = f"🔁 Сменяемый | Остаток: {stock}"
        else:
            type_text = "📌 Статичный"

        text += (
            f"{status} <b>{product['name']}</b>\n"
            f"ID: <code>{product['id']}</code>\n"
            f"Категория: {product['category']}\n"
            f"Цена: {product['price']} ₽\n"
            f"Тип: {type_text}\n\n"
        )

    await callback.message.edit_text(
        text,
        reply_markup=admin_menu()
    )

    await callback.answer()


@router.callback_query(F.data == "admin_add_balance")
async def admin_add_balance(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return

    await state.set_state(ChangeBalance.user_id)
    await state.update_data(action="add")

    await callback.message.edit_text(
        "💰 <b>Пополнение баланса</b>\n\n"
        "Введите Telegram ID пользователя:"
    )

    await callback.answer()


@router.callback_query(F.data == "admin_remove_balance")
async def admin_remove_balance(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return

    await state.set_state(ChangeBalance.user_id)
    await state.update_data(action="remove")

    await callback.message.edit_text(
        "➖ <b>Списание баланса</b>\n\n"
        "Введите Telegram ID пользователя:"
    )

    await callback.answer()


@router.message(ChangeBalance.user_id)
async def change_balance_user_id(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❗ ID должен быть числом. Введите Telegram ID:")
        return

    await state.update_data(user_id=int(message.text))
    await state.set_state(ChangeBalance.amount)

    await message.answer("Введите сумму:")


@router.message(ChangeBalance.amount)
async def change_balance_amount(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❗ Сумма должна быть числом. Введите сумму:")
        return

    data = await state.get_data()

    user_id = data["user_id"]
    amount = int(message.text)
    action = data["action"]

    if action == "add":
        balance = add_balance(user_id, amount)
        text = "✅ Баланс пополнен."
    else:
        balance = remove_balance(user_id, amount)
        text = "✅ Баланс списан."

    await state.clear()

    await message.answer(
        f"{text}\n\n"
        f"👤 User ID: <code>{user_id}</code>\n"
        f"💰 Текущий баланс: {balance} ₽",
        reply_markup=admin_menu()
    )


@router.callback_query(F.data == "admin_delete_product")
async def admin_delete_product(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return

    products = load_products()
    active_products = [p for p in products if p.get("active")]

    if not active_products:
        await callback.message.edit_text(
            "🗑 Активных товаров для удаления нет.",
            reply_markup=admin_menu()
        )
        await callback.answer()
        return

    text = "🗑 <b>Удаление товара</b>\n\nВыберите ID товара из списка:\n\n"

    for product in active_products:
        text += (
            f"📦 <b>{product['name']}</b>\n"
            f"ID: <code>{product['id']}</code>\n"
            f"Категория: {product['category']}\n"
            f"Цена: {product['price']} ₽\n\n"
        )

    await state.set_state(DeleteProduct.product_id)

    await callback.message.edit_text(text)

    await callback.answer()


@router.message(DeleteProduct.product_id)
async def delete_product_by_id(message: Message, state: FSMContext):
    product_id = message.text.strip()

    result = delete_product(product_id)

    await state.clear()

    if result:
        await message.answer(
            f"✅ Товар <code>{product_id}</code> удалён из каталога.",
            reply_markup=admin_menu()
        )
    else:
        await message.answer(
            "❌ Товар с таким ID не найден.",
            reply_markup=admin_menu()
        )


@router.callback_query(F.data == "admin_add_promo")
async def admin_add_promo(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return

    await state.set_state(AddPromo.code)

    await callback.message.edit_text(
        "🎁 <b>Добавление промокода</b>\n\n"
        "Введите название промокода:"
    )

    await callback.answer()


@router.message(AddPromo.code)
async def add_promo_code(message: Message, state: FSMContext):
    await state.update_data(code=message.text.strip().upper())
    await state.set_state(AddPromo.amount)

    await message.answer("Введите сумму, которая будет начислена:")


@router.message(AddPromo.amount)
async def add_promo_amount(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❗ Сумма должна быть числом.")
        return

    data = await state.get_data()

    code = data["code"]
    amount = int(message.text)

    add_promocode(code, amount)

    await state.clear()

    await message.answer(
        f"✅ <b>Промокод создан</b>\n\n"
        f"🎁 Код: <code>{code}</code>\n"
        f"💰 Сумма: {amount} ₽\n\n"
        f"⚠️ Промокод одноразовый.",
        reply_markup=admin_menu()
    )