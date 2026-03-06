"""
Qishloq-AI Menu Handler
Asosiy menyu va callback routing
"""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.inline import main_menu_keyboard

router = Router()


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    """Menyu buyrug'i"""
    await message.answer(
        "🌾 <b>Qishloq-AI — Asosiy Menyu</b>\n\n"
        "Quyidagi xizmatlardan birini tanlang 👇\n\n"
        "💡 <i>Har bir bo'limda AI asosida tavsiyalar olasiz</i>",
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "menu:main")
async def callback_main_menu(callback: CallbackQuery):
    """Asosiy menyuga qaytish"""
    await callback.message.edit_text(
        "🌾 <b>Qishloq-AI — Asosiy Menyu</b>\n\n"
        "Quyidagi xizmatlardan birini tanlang 👇\n\n"
        "💡 <i>Har bir bo'limda AI asosida tavsiyalar olasiz</i>",
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "menu:help")
async def callback_help(callback: CallbackQuery):
    """Yordam menyusi"""
    await callback.message.edit_text(
        "📖 <b>Qishloq-AI — Yordam</b>\n\n"
        "🤖 <b>Buyruqlar:</b>\n"
        "  /start — Botni boshlash\n"
        "  /help — Yordam\n"
        "  /menu — Asosiy menyu\n"
        "  /profile — Profilim\n"
        "  /weather — Ob-havo\n"
        "  /soil — Tuproq tahlili\n"
        "  /market — Bozor narxlari\n\n"
        "🌱 <b>Xizmatlar:</b>\n"
        "  🌱 Tuproq Monitoring — tuproq parametrlarini kiriting\n"
        "  💧 Sug'orish — qachon sug'orish kerakligi\n"
        "  🧪 O'g'itlash — qanday o'g'it kerakligi\n"
        "  🌾 Ekin — viloyat va tuproqqa mos ekinlar\n"
        "  🔬 Kasallik — rasm yuboring, AI tahlil qiladi\n"
        "  ⛅ Ob-havo — ob-havo prognozi\n"
        "  💰 Narxlar — mahsulot narxlari\n\n"
        "❓ <b>Savol:</b> @QishloqAI_support",
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "menu:stats")
async def callback_stats(callback: CallbackQuery):
    """Statistika"""
    from sqlalchemy import select, func
    from database.db import async_session
    from database.models import User, SoilRecord, Consultation

    async with async_session() as session:
        # Foydalanuvchilar soni
        users_count = await session.scalar(select(func.count(User.id)))
        # Tuproq yozuvlari
        soil_count = await session.scalar(select(func.count(SoilRecord.id)))
        # Maslahatlar
        consult_count = await session.scalar(select(func.count(Consultation.id)))

    await callback.message.edit_text(
        "📊 <b>Qishloq-AI Statistika</b>\n\n"
        f"👥 Jami foydalanuvchilar: <b>{users_count}</b>\n"
        f"🌱 Tuproq tahlillari: <b>{soil_count}</b>\n"
        f"💬 Maslahatlar: <b>{consult_count}</b>\n\n"
        "🌾 <i>Qishloq-AI — har bir dehqon uchun AI maslahatchisi</i>",
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()
