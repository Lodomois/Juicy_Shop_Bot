from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from config.config import MANAGER_USERNAME

from bot.keyboards.profile_menu import profile_menu
from bot.states.profile_states import PromoState
from services.shop_service import get_user, toggle_language, activate_promocode

router = Router()


@router.callback_query(F.data == "profile")
async def open_profile(callback: CallbackQuery):
    tg_user = callback.from_user
    user_data = get_user(tg_user.id)

    text = (
        f"👤 <b>Профиль</b>\n\n"
        f"Username: @{tg_user.username or 'не указан'}\n"
        f"ID: <code>{tg_user.id}</code>\n\n"
        f"💵 Баланс: {user_data['balance']} ₽\n"
        f"📦 Покупок: {len(user_data['purchases'])}\n"
        f"🌐 Язык: {user_data.get('language', 'ru').upper()}"
    )

    await callback.message.edit_text(
        text=text,
        reply_markup=profile_menu()
    )

    await callback.answer()


@router.message(F.text == "👤 Профиль")
async def profile_message_handler(message: Message):
    tg_user = message.from_user
    user_data = get_user(tg_user.id)

    text = (
        f"👤 <b>Профиль</b>\n\n"
        f"Username: @{tg_user.username or 'не указан'}\n"
        f"ID: <code>{tg_user.id}</code>\n\n"
        f"💵 Баланс: {user_data['balance']} ₽\n"
        f"📦 Покупок: {len(user_data['purchases'])}\n"
        f"🌐 Язык: {user_data.get('language', 'ru').upper()}"
    )

    await message.answer(
        text=text,
        reply_markup=profile_menu()
    )

@router.callback_query(F.data == "deposit")
async def deposit_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        "💳 <b>Пополнение баланса</b>\n\n"
        f"Для пополнения баланса обращайтесь сюда - @{MANAGER_USERNAME}",
        reply_markup=profile_menu()
    )

    await callback.answer()


@router.callback_query(F.data == "language")
async def language_handler(callback: CallbackQuery):
    new_language = toggle_language(callback.from_user.id)

    if new_language == "ru":
        text = "🌐 Язык изменён на Русский 🇷🇺"
    else:
        text = "🌐 Language changed to English 🇬🇧"

    await callback.answer(text, show_alert=True)

    await open_profile(callback)


@router.callback_query(F.data == "promo")
async def promo_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(PromoState.code)

    await callback.message.edit_text(
        "🎁 <b>Активация промокода</b>\n\n"
        "Введите промокод:"
    )

    await callback.answer()


@router.message(PromoState.code)
async def promo_code_handler(message: Message, state: FSMContext):
    success, text = activate_promocode(
        user_id=message.from_user.id,
        code=message.text.strip()
    )

    await state.clear()

    await message.answer(
        text,
        reply_markup=profile_menu()
    )


@router.callback_query(F.data == "purchases")
async def purchases_handler(callback: CallbackQuery):
    user_data = get_user(callback.from_user.id)
    purchases = user_data.get("purchases", [])

    if not purchases:
        await callback.message.edit_text(
            "📦 <b>Мои покупки</b>\n\n"
            "У вас пока нет покупок.",
            reply_markup=profile_menu()
        )
        await callback.answer()
        return

    text = "📦 <b>Мои покупки</b>\n\n"

    for index, purchase in enumerate(purchases, start=1):
        if isinstance(purchase, dict):
            text += (
                f"{index}. <b>{purchase.get('name', 'Товар')}</b>\n"
                f"💰 Цена: {purchase.get('price', 0)} ₽\n"
                f"📦 Выдача: <code>{purchase.get('content', '—')}</code>\n\n"
            )
        else:
            text += f"{index}. Товар ID: <code>{purchase}</code>\n\n"

    await callback.message.edit_text(
        text,
        reply_markup=profile_menu()
    )

    await callback.answer()