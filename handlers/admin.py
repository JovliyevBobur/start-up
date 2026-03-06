"""
Qishloq-AI Admin Handler
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy import select, func

from database.db import async_session
from database.models import User, SoilRecord, Consultation
from keyboards.inline import admin_keyboard, main_menu_keyboard
from config import ADMIN_IDS

router = Router()


class AdminStates(StatesGroup):
    waiting_broadcast = State()


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


@router.message(F.text == "/admin")
async def cmd_admin(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Sizda admin huquqi yo'q.")
        return
    await message.answer(
        "🔧 <b>Admin Panel</b>\n\nBoshqaruv menyusi:",
        reply_markup=admin_keyboard(),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "admin:users_count")
async def admin_users_count(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Admin huquqi kerak", show_alert=True)
        return

    async with async_session() as session:
        total = await session.scalar(select(func.count(User.id)))
        premium = await session.scalar(
            select(func.count(User.id)).where(User.is_premium == True)
        )

    await callback.message.edit_text(
        f"👥 <b>Foydalanuvchilar</b>\n\n"
        f"  📊 Jami: <b>{total}</b>\n"
        f"  ⭐ Premium: <b>{premium}</b>\n"
        f"  👤 Oddiy: <b>{total - premium}</b>",
        reply_markup=admin_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "admin:statistics")
async def admin_statistics(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Admin huquqi kerak", show_alert=True)
        return

    async with async_session() as session:
        users = await session.scalar(select(func.count(User.id)))
        soils = await session.scalar(select(func.count(SoilRecord.id)))
        consults = await session.scalar(select(func.count(Consultation.id)))

        # Maslahat turlari bo'yicha
        types = {}
        for t in ["soil", "irrigation", "fertilizer", "crop", "disease", "weather"]:
            cnt = await session.scalar(
                select(func.count(Consultation.id))
                .where(Consultation.consultation_type == t)
            )
            types[t] = cnt

    type_names = {
        "soil": "🌱 Tuproq", "irrigation": "💧 Sug'orish",
        "fertilizer": "🧪 O'g'itlash", "crop": "🌾 Ekin",
        "disease": "🔬 Kasallik", "weather": "⛅ Ob-havo",
    }

    msg = f"📊 <b>Batafsil Statistika</b>\n"
    msg += "━" * 28 + "\n\n"
    msg += f"👥 Foydalanuvchilar: <b>{users}</b>\n"
    msg += f"🌱 Tuproq yozuvlari: <b>{soils}</b>\n"
    msg += f"💬 Jami maslahatlar: <b>{consults}</b>\n\n"
    msg += "<b>Maslahat turlari:</b>\n"
    for t, name in type_names.items():
        msg += f"  {name}: <b>{types.get(t, 0)}</b>\n"

    await callback.message.edit_text(msg, reply_markup=admin_keyboard(), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "admin:broadcast")
async def admin_broadcast(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Admin huquqi kerak", show_alert=True)
        return

    await callback.message.edit_text(
        "📢 <b>Broadcast xabar</b>\n\n"
        "Barcha foydalanuvchilarga yuboriladigan\n"
        "xabarni yozing:\n\n"
        "<i>Bekor qilish uchun /menu yuboring</i>",
        parse_mode="HTML",
    )
    await state.set_state(AdminStates.waiting_broadcast)
    await callback.answer()


@router.message(AdminStates.waiting_broadcast)
async def process_broadcast(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    if message.text == "/menu":
        await state.clear()
        await message.answer("❌ Broadcast bekor qilindi.", reply_markup=main_menu_keyboard())
        return

    async with async_session() as session:
        result = await session.execute(select(User.telegram_id))
        user_ids = [row[0] for row in result.all()]

    success = 0
    failed = 0
    for uid in user_ids:
        try:
            await message.bot.send_message(
                uid,
                f"📢 <b>Qishloq-AI xabari:</b>\n\n{message.text}",
                parse_mode="HTML",
            )
            success += 1
        except Exception:
            failed += 1

    await state.clear()
    await message.answer(
        f"📢 <b>Broadcast yakunlandi!</b>\n\n"
        f"  ✅ Yuborildi: {success}\n"
        f"  ❌ Xato: {failed}\n"
        f"  📊 Jami: {len(user_ids)}",
        reply_markup=admin_keyboard(),
        parse_mode="HTML",
    )
