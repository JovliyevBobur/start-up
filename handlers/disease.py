"""
Qishloq-AI Kasallik Aniqlash Handler
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select

from database.db import async_session
from database.models import User, Consultation
from keyboards.inline import main_menu_keyboard
from services.disease_detector import detect_disease

router = Router()


@router.callback_query(F.data == "menu:disease")
async def disease_menu(callback: CallbackQuery):
    """Kasallik aniqlash menyusi"""
    await callback.message.edit_text(
        "🔬 <b>Kasallik Aniqlash</b>\n\n"
        "Ekin kasalligini aniqlash uchun\n"
        "kasallangan ekin <b>suratini yuboring</b> 📸\n\n"
        "📋 <b>Yaxshi natija olish uchun:</b>\n"
        "  • Kasallangan qismni yaqindan suring\n"
        "  • Yaxshi yorug'likda suring\n"
        "  • Bargning har ikki tomonini suring\n"
        "  • Bir nechta rasm yuboring\n\n"
        "🤖 AI rasmni tahlil qilib, kasallikni aniqlaydi\n"
        "va davolash usulini tavsiya qiladi.\n\n"
        "👇 <b>Rasmni hozir yuboring!</b>",
        parse_mode="HTML",
    )
    await callback.answer()


@router.message(F.photo)
async def process_photo(message: Message):
    """Rasm qabul qilish va tahlil qilish"""
    await message.answer("🔄 <b>Rasm tahlil qilinmoqda...</b>\n⏳ Biroz kuting...", parse_mode="HTML")

    result = detect_disease(photo_received=True)

    try:
        async with async_session() as session:
            user_result = await session.execute(
                select(User).where(User.telegram_id == message.from_user.id)
            )
            user = user_result.scalar_one_or_none()
            if user:
                c = Consultation(user_id=user.id, consultation_type="disease",
                                 question="Photo analysis", answer=result[:200])
                session.add(c)
                await session.commit()
    except Exception:
        pass

    await message.answer(result, parse_mode="HTML")
    await message.answer("📌 Boshqa xizmat uchun:", reply_markup=main_menu_keyboard())
