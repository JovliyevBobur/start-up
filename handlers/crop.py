"""
Qishloq-AI Ekin Tanlash Handler
"""
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy import select

from database.db import async_session
from database.models import User, Consultation
from keyboards.inline import viloyat_keyboard, tuproq_keyboard, main_menu_keyboard
from config import VILOYATLAR, TUPROQ_TURLARI
from services.crop_advisor import get_crop_recommendation

router = Router()


class CropStates(StatesGroup):
    waiting_region = State()
    waiting_soil = State()


@router.callback_query(F.data == "menu:crop")
async def crop_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    # Check if user has region set
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = result.scalar_one_or_none()

    if user and user.region and user.soil_type:
        msg = get_crop_recommendation(user.region, user.soil_type)
        await callback.message.edit_text(msg, parse_mode="HTML")
        await callback.message.answer(
            "📌 Boshqa viloyat uchun tavsiya olish yoki menyuga qaytish:",
            reply_markup=main_menu_keyboard(),
        )
        try:
            async with async_session() as session:
                c = Consultation(user_id=user.id, consultation_type="crop",
                                 question=f"{user.region}, {user.soil_type}")
                session.add(c)
                await session.commit()
        except Exception:
            pass
    else:
        await callback.message.edit_text(
            "🌾 <b>Ekin Tanlash Tavsiyasi</b>\n\n"
            "Viloyatingizni tanlang — AI sizga mos ekinlarni tavsiya qiladi:\n\n"
            "  🌱 Mintaqaga mos ekinlar\n"
            "  🏔 Tuproqqa mos ekinlar\n"
            "  📅 Mavsumga qarab ekish vaqti\n\n"
            "👇 Viloyatni tanlang:",
            reply_markup=viloyat_keyboard("crop_region"),
            parse_mode="HTML",
        )
        await state.set_state(CropStates.waiting_region)
    await callback.answer()


@router.callback_query(CropStates.waiting_region, F.data.startswith("crop_region:"))
async def process_crop_region(callback: CallbackQuery, state: FSMContext):
    idx = int(callback.data.split(":")[1])
    region = VILOYATLAR[idx]
    await state.update_data(region=region)

    await callback.message.edit_text(
        f"📍 Viloyat: <b>{region}</b>\n\n"
        "🏔 Endi tuproq turini tanlang:",
        reply_markup=tuproq_keyboard("crop_soil"),
        parse_mode="HTML",
    )
    await state.set_state(CropStates.waiting_soil)
    await callback.answer()


@router.callback_query(CropStates.waiting_soil, F.data.startswith("crop_soil:"))
async def process_crop_soil(callback: CallbackQuery, state: FSMContext):
    idx = int(callback.data.split(":")[1])
    soil = TUPROQ_TURLARI[idx]
    data = await state.get_data()
    region = data.get("region")

    msg = get_crop_recommendation(region, soil)
    await state.clear()
    await callback.message.edit_text(msg, parse_mode="HTML")
    await callback.message.answer("📌 Menyuga qaytish:", reply_markup=main_menu_keyboard())
    await callback.answer()
