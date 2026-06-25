import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from config.config import BOT_TOKEN

from bot.handlers.start import router as start_router
from bot.handlers.menu import router as menu_router
from bot.handlers.catalog import router as catalog_router
from bot.handlers.profile import router as profile_router
from bot.handlers.admin import router as admin_router


async def main():

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode="HTML"
        )
    )

    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(menu_router)
    dp.include_router(catalog_router)
    dp.include_router(profile_router)
    dp.include_router(admin_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())