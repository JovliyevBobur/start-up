"""
Qishloq-AI Sug'orish Tavsiyasi Handler
"""
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy import select

from database.db import async_session
from database.models import User, Consultation
from keyboards.inline import ekin_keyboard, irrigation_method_keyboard, main_menu_keyboard
from config import EKIN_TURLARI
from utils.helpers import get_season

router = Router()


class IrrigationStates(StatesGroup):
    waiting_crop = State()


IRRIGATION_NORMS = {
    "Bug'doy": {"norm": 600, "freq": "10-15 kun", "total": 4500, "method": "Egatma"},
    "Paxta": {"norm": 800, "freq": "8-12 kun", "total": 6000, "method": "Egatma/Tomchilatib"},
    "Pomidor": {"norm": 500, "freq": "5-7 kun", "total": 5500, "method": "Tomchilatib"},
    "Bodring": {"norm": 400, "freq": "3-5 kun", "total": 4000, "method": "Tomchilatib"},
    "Makkajo'xori": {"norm": 700, "freq": "10-14 kun", "total": 4000, "method": "Egatma"},
    "Uzum": {"norm": 500, "freq": "12-18 kun", "total": 3000, "method": "Tomchilatib"},
    "Olma": {"norm": 600, "freq": "14-20 kun", "total": 3500, "method": "Tomchilatib"},
    "Shaftoli": {"norm": 550, "freq": "12-16 kun", "total": 3200, "method": "Tomchilatib"},
    "Kartoshka": {"norm": 500, "freq": "7-10 kun", "total": 4000, "method": "Tomchilatib"},
    "Piyoz": {"norm": 350, "freq": "5-8 kun", "total": 3500, "method": "Egatma/Tomchilatib"},
    "Sabzi": {"norm": 400, "freq": "6-8 kun", "total": 3800, "method": "Tomchilatib"},
    "Qalampir": {"norm": 450, "freq": "5-7 kun", "total": 4500, "method": "Tomchilatib"},
    "Qovun": {"norm": 500, "freq": "8-12 kun", "total": 3000, "method": "Egatma"},
    "Tarvuz": {"norm": 500, "freq": "8-12 kun", "total": 2800, "method": "Egatma"},
    "Kungaboqar": {"norm": 600, "freq": "12-15 kun", "total": 3000, "method": "Egatma"},
}


@router.callback_query(F.data == "menu:irrigation")
async def irrigation_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "💧 <b>Sug'orish Tavsiyasi</b>\n\n"
        "Ekin turini tanlang — AI sizga:\n"
        "  💦 Qancha suv kerak\n"
        "  ⏰ Qachon sug'orish kerak\n"
        "  📊 Qaysi usul samaraliroq\n\n"
        "👇 Ekin turini tanlang:",
        reply_markup=ekin_keyboard("irr_crop"),
        parse_mode="HTML",
    )
    await state.set_state(IrrigationStates.waiting_crop)
    await callback.answer()


@router.callback_query(IrrigationStates.waiting_crop, F.data.startswith("irr_crop:"))
async def process_irrigation_crop(callback: CallbackQuery, state: FSMContext):
    idx = int(callback.data.split(":")[1])
    crop_full = EKIN_TURLARI[idx]
    crop_name = crop_full.split(" ", 1)[1] if " " in crop_full else crop_full
    norm = IRRIGATION_NORMS.get(crop_name, {"norm": 500, "freq": "7-10 kun", "total": 4000, "method": "Tomchilatib"})
    season = get_season()

    msg = f"💧 <b>Sug'orish Tavsiyasi — {crop_full}</b>\n"
    msg += f"📅 Mavsum: {season}\n"
    msg += "━" * 30 + "\n\n"
    msg += f"📊 <b>Sug'orish me'yori:</b>\n"
    msg += f"  💦 Bir sug'orishda: <b>{norm['norm']} m³/ga</b>\n"
    msg += f"  ⏰ Oraliq: <b>{norm['freq']}</b>\n"
    msg += f"  📈 Mavsumlik jami: <b>{norm['total']} m³/ga</b>\n"
    msg += f"  🔧 Tavsiya usul: <b>{norm['method']}</b>\n\n"

    msg += f"🔄 <b>Usullar samaradorligi:</b>\n"
    msg += f"  💧 Tomchilatib:  90-95% samarali\n"
    msg += f"  🌧 Yomg'irlatib: 70-80% samarali\n"
    msg += f"  🌊 Egatma:       40-50% samarali\n\n"

    msg += f"📌 <b>Amaliy maslahatlar:</b>\n"
    msg += f"  🕐 Eng yaxshi: ertalab 06-08 yoki kechqurun 18-20\n"
    msg += f"  🚫 Kunduzi (11-16) sug'ormang — suv isrof\n"
    msg += f"  🌿 Mulchalash sarf ni 30-40% kamaytiradi\n"
    msg += f"  📏 Tuproq 20-30 cm ga namlaning\n\n"

    msg += f"💰 <b>Tomchilatib sug'orishga o'tsangiz:</b>\n"
    msg += f"  💧 Suv tejash: ~40-50%\n"
    msg += f"  📈 Hosil oshishi: ~20-30%\n"
    msg += f"  💵 Xarajat tejash: ~35%\n"
    msg += "\n" + "━" * 30 + "\n"
    msg += "🤖 <i>Aniqroq tavsiya uchun tuproq namligini kiriting</i>"

    try:
        async with async_session() as session:
            ur = await session.execute(select(User).where(User.telegram_id == callback.from_user.id))
            user = ur.scalar_one_or_none()
            if user:
                c = Consultation(user_id=user.id, consultation_type="irrigation",
                                 question=crop_name, answer=f"{norm['norm']} m³/ga, {norm['freq']}")
                session.add(c)
                await session.commit()
    except Exception:
        pass

    await state.clear()
    await callback.message.edit_text(msg, parse_mode="HTML")
    await callback.message.answer("📌 Menyudan tanlang:", reply_markup=main_menu_keyboard())
    await callback.answer()


@router.callback_query(F.data.startswith("irr_method:"))
async def irrigation_method_info(callback: CallbackQuery):
    method = callback.data.split(":")[1]
    methods = {
        "drip": (
            "💧 <b>Tomchilatib Sug'orish</b>\n\n"
            "📊 Samaradorlik: 90-95%\n💰 Xarajat: $800-1500/ga\n\n"
            "✅ Afzalliklari:\n• Suv 40-50% tejaladi\n• Hosil 20-30% oshadi\n"
            "• Fertigatsiya imkoniyati\n• Begona o't kamayadi\n\n"
            "❌ Kamchiliklari:\n• Boshlang'ich xarajat yuqori\n• Texnik xizmat kerak"
        ),
        "furrow": (
            "🌊 <b>Egatma Sug'orish</b>\n\n"
            "📊 Samaradorlik: 40-50%\n💰 Xarajat: $100-300/ga\n\n"
            "✅ Afzalliklari:\n• Arzon va oddiy\n• Maxsus uskuna kerak emas\n\n"
            "❌ Kamchiliklari:\n• 50-60% suv yo'qotish\n• Sho'rlanish xavfi"
        ),
        "sprinkler": (
            "🌧 <b>Yomg'irlatib Sug'orish</b>\n\n"
            "📊 Samaradorlik: 70-80%\n💰 Xarajat: $500-1000/ga\n\n"
            "✅ Afzalliklari:\n• Tekis sug'orish\n• Katta maydon uchun mos\n\n"
            "❌ Kamchiliklari:\n• Shamolda samaradorlik tushadi\n• Energiya sarfi yuqori"
        ),
        "ai_suggest": (
            "🤖 <b>AI Tavsiyasi</b>\n\n"
            "O'zbekiston uchun eng samarali:\n\n"
            "1️⃣ Tomchilatib — sabzavot/mevalar uchun\n"
            "2️⃣ Yomg'irlatib — katta maydonlar uchun\n"
            "3️⃣ Egatma — sholi uchun\n\n"
            "💡 Hukumat subsidiyasi: narxning 30-50% qoplanadi!"
        ),
    }
    text = methods.get(method, "Ma'lumot topilmadi")
    await callback.message.edit_text(text, reply_markup=main_menu_keyboard(), parse_mode="HTML")
    await callback.answer()
