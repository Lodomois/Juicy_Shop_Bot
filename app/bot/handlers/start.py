from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.keyboards.main_menu import main_menu
from bot.keyboards.reply_menu import reply_main_menu
from services.shop_service import get_user

router = Router()


@router.message(CommandStart())
async def start(message: Message):

    get_user(message.from_user.id)

    await message.answer(
        "🏠 <b>Главное меню</b>",
        reply_markup=reply_main_menu()
    )

    await message.answer(
        "Выберите раздел:",
        reply_markup=main_menu()
    )