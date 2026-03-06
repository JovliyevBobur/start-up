"""
🌾 Qishloq-AI Telegram Bot
O'zbekiston dehqonlari uchun AI tuproq maslahatchisi

Ishga tushirish:
    1. .env fayliga BOT_TOKEN yozing
    2. pip install -r requirements.txt
    3. python bot.py
"""
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from database.db import init_db
from middlewares.throttling import ThrottlingMiddleware

# Handlers
from handlers import start, menu, soil, irrigation, fertilizer
from handlers import crop, disease, weather, market, profile, admin


async def main():
    """Botni ishga tushirish"""
    # Logging (UTF-8 for Windows compatibility)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    except Exception:
        pass
    logging.basicConfig(level=logging.INFO, handlers=[handler])
    logger = logging.getLogger(__name__)

    # Token tekshirish
    if not BOT_TOKEN or BOT_TOKEN == "your_bot_token_here":
        logger.error("BOT_TOKEN topilmadi!")
        logger.error("   .env fayliga BOT_TOKEN=your_token yozing")
        logger.error("   yoki .env.example dan nusxa oling: copy .env.example .env")
        sys.exit(1)

    # Database
    logger.info("Ma'lumotlar bazasi tayyorlanmoqda...")
    await init_db()
    logger.info("Ma'lumotlar bazasi tayyor!")

    # Bot va Dispatcher
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())

    # Middleware
    dp.message.middleware(ThrottlingMiddleware(rate_limit=0.5))

    # Routerlarni ro'yxatdan o'tkazish
    dp.include_router(start.router)
    dp.include_router(menu.router)
    dp.include_router(soil.router)
    dp.include_router(irrigation.router)
    dp.include_router(fertilizer.router)
    dp.include_router(crop.router)
    dp.include_router(disease.router)
    dp.include_router(weather.router)
    dp.include_router(market.router)
    dp.include_router(profile.router)
    dp.include_router(admin.router)

    # Bot ma'lumotlari
    logger.info("Qishloq-AI Bot ishga tushmoqda...")
    logger.info("Bot: @QishloqAI_bot")
    logger.info("Buyruqlar: /start, /help, /menu, /soil, /weather, /market, /profile, /admin")

    # Polling boshlash
    try:
        # Eski webhook'ni o'chirish
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
