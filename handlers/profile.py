"""
Qishloq-AI Profil Handler
"""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy import select

from database.db import async_session
from database.models import User, Consultation
from keyboards.inline import profile_keyboard, viloyat_keyboard, main_menu_keyboard
from config import VILOYATLAR

router = Router()


class ProfileEditStates(StatesGroup):
    editing_name = State()
    editing_region = State()
    editing_farm = State()
    editing_crops = State()


@router.callback_query(F.data == "menu:profile")
async def profile_menu(callback: CallbackQuery):
    await show_profile(callback)


@router.message(Command("profile"))
async def cmd_profile(message: Message):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()

    if not user:
        await message.answer("❌ Siz hali ro'yxatdan o'tmagansiz. /start buyrug'ini yuboring.")
        return

    msg = format_profile(user)
    await message.answer(msg, reply_markup=profile_keyboard(), parse_mode="HTML")


async def show_profile(callback: CallbackQuery):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = result.scalar_one_or_none()

    if not user:
        await callback.message.edit_text(
            "❌ Siz hali ro'yxatdan o'tmagansiz.\n/start buyrug'ini yuboring.",
        )
        await callback.answer()
        return

    msg = format_profile(user)
    await callback.message.edit_text(msg, reply_markup=profile_keyboard(), parse_mode="HTML")
    await callback.answer()


def format_profile(user) -> str:
    return (
        f"👤 <b>Mening Profilim</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"  👤 <b>Ism:</b> {user.full_name}\n"
        f"  📱 <b>Telefon:</b> {user.phone or 'Kiritilmagan'}\n"
        f"  📍 <b>Viloyat:</b> {user.region or 'Belgilanmagan'}\n"
        f"  🏞 <b>Yer maydoni:</b> {user.farm_size or 0} ga\n"
        f"  🏔 <b>Tuproq turi:</b> {user.soil_type or 'Belgilanmagan'}\n"
        f"  🌱 <b>Ekinlar:</b> {user.main_crops or 'Kiritilmagan'}\n"
        f"  ⭐ <b>Status:</b> {'Premium ✨' if user.is_premium else 'Oddiy'}\n"
        f"  📅 <b>Ro\\'yxatdan:</b> {user.registered_at.strftime('%d.%m.%Y') if user.registered_at else '-'}\n\n"
        f"✏️ Ma'lumotlarni o'zgartirish uchun quyidagi tugmalarni bosing:"
    )


@router.callback_query(F.data == "profile:edit_name")
async def edit_name(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "✏️ <b>Yangi ism-familiyangizni kiriting:</b>",
        parse_mode="HTML",
    )
    await state.set_state(ProfileEditStates.editing_name)
    await callback.answer()


@router.message(ProfileEditStates.editing_name)
async def process_edit_name(message: Message, state: FSMContext):
    if len(message.text) < 3:
        await message.answer("❌ Ism juda qisqa. Qayta kiriting:")
        return
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()
        if user:
            user.full_name = message.text
            await session.commit()
    await state.clear()
    await message.answer(
        f"✅ Ismingiz <b>{message.text}</b> ga o'zgartirildi!",
        reply_markup=profile_keyboard(),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "profile:edit_region")
async def edit_region(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "📍 <b>Yangi viloyatni tanlang:</b>",
        reply_markup=viloyat_keyboard("profile_region"),
        parse_mode="HTML",
    )
    await state.set_state(ProfileEditStates.editing_region)
    await callback.answer()


@router.callback_query(ProfileEditStates.editing_region, F.data.startswith("profile_region:"))
async def process_edit_region(callback: CallbackQuery, state: FSMContext):
    idx = int(callback.data.split(":")[1])
    region = VILOYATLAR[idx]
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = result.scalar_one_or_none()
        if user:
            user.region = region
            await session.commit()
    await state.clear()
    await callback.message.edit_text(
        f"✅ Viloyat <b>{region}</b> ga o'zgartirildi!",
        reply_markup=profile_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "profile:edit_farm")
async def edit_farm(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "🏞 <b>Yer maydoningiz (ga):</b>\nRaqam kiriting:",
        parse_mode="HTML",
    )
    await state.set_state(ProfileEditStates.editing_farm)
    await callback.answer()


@router.message(ProfileEditStates.editing_farm)
async def process_edit_farm(message: Message, state: FSMContext):
    try:
        size = float(message.text.replace(",", "."))
        if size <= 0:
            raise ValueError()
    except ValueError:
        await message.answer("❌ Noto'g'ri raqam. Qayta kiriting:")
        return
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()
        if user:
            user.farm_size = size
            await session.commit()
    await state.clear()
    await message.answer(
        f"✅ Yer maydoni <b>{size} ga</b> ga o'zgartirildi!",
        reply_markup=profile_keyboard(),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "profile:edit_crops")
async def edit_crops(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "🌱 <b>Asosiy ekinlaringizni yozing:</b>\n"
        "(vergul bilan ajrating)\n"
        "Masalan: <i>bug'doy, paxta, pomidor</i>",
        parse_mode="HTML",
    )
    await state.set_state(ProfileEditStates.editing_crops)
    await callback.answer()


@router.message(ProfileEditStates.editing_crops)
async def process_edit_crops(message: Message, state: FSMContext):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()
        if user:
            user.main_crops = message.text
            await session.commit()
    await state.clear()
    await message.answer(
        f"✅ Ekinlar saqlandi: <b>{message.text}</b>",
        reply_markup=profile_keyboard(),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "profile:history")
async def consultation_history(callback: CallbackQuery):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = result.scalar_one_or_none()

    if not user:
        await callback.answer("❌ Profil topilmadi", show_alert=True)
        return

    async with async_session() as session:
        from sqlalchemy import desc
        result = await session.execute(
            select(Consultation)
            .where(Consultation.user_id == user.id)
            .order_by(desc(Consultation.created_at))
            .limit(10)
        )
        consultations = result.scalars().all()

    if not consultations:
        await callback.message.edit_text(
            "📋 <b>Maslahat tarixi</b>\n\nHali maslahat olmadingiz.",
            reply_markup=main_menu_keyboard(),
            parse_mode="HTML",
        )
        await callback.answer()
        return

    type_names = {
        "soil": "🌱 Tuproq", "irrigation": "💧 Sug'orish",
        "fertilizer": "🧪 O'g'itlash", "crop": "🌾 Ekin",
        "disease": "🔬 Kasallik", "weather": "⛅ Ob-havo",
    }

    msg = "📋 <b>Maslahat Tarixi</b> (oxirgi 10 ta)\n"
    msg += "━" * 28 + "\n\n"
    for c in consultations:
        t = type_names.get(c.consultation_type, c.consultation_type)
        date = c.created_at.strftime("%d.%m.%Y %H:%M") if c.created_at else "-"
        msg += f"  {t} — {date}\n"
        if c.question:
            msg += f"  💬 {c.question[:50]}\n"
        msg += "\n"

    await callback.message.edit_text(msg, reply_markup=profile_keyboard(), parse_mode="HTML")
    await callback.answer()
