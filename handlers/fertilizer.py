"""
Qishloq-AI O'g'itlash Tavsiyasi Handler
"""
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy import select

from database.db import async_session
from database.models import User, Consultation
from keyboards.inline import ekin_keyboard, main_menu_keyboard
from config import EKIN_TURLARI

router = Router()


class FertilizerStates(StatesGroup):
    waiting_crop = State()


FERTILIZER_NORMS = {
    "Bug'doy": {
        "N": 180, "P": 90, "K": 60,
        "schedule": [
            ("Ekishdan oldin", "Superfosfat 200 kg/ga, Kaliy xlorid 100 kg/ga"),
            ("Tuplanish", "Ammoniy selitra 150 kg/ga"),
            ("Boshoqlash", "Karbamid 50 kg/ga (bargdan purkash)"),
        ],
        "organic": "Chirigan go'ng 20-30 t/ga (kuzda)",
    },
    "Paxta": {
        "N": 200, "P": 140, "K": 100,
        "schedule": [
            ("Ekishdan oldin", "Superfosfat 300 kg/ga, Kaliy 150 kg/ga"),
            ("2-3 chinbarg", "Ammoniy selitra 150 kg/ga"),
            ("Gullash", "Karbamid 100 kg/ga"),
            ("Ko'sak", "Kaliy sulfat 50 kg/ga"),
        ],
        "organic": "Chirigan go'ng 25-30 t/ga",
    },
    "Pomidor": {
        "N": 150, "P": 100, "K": 180,
        "schedule": [
            ("Ko'chat ekishda", "Superfosfat 50 g/tuynukka"),
            ("Gullash", "Ammoniy selitra 200 kg/ga"),
            ("Meva tugish", "Kaliy sulfat 150 kg/ga"),
            ("Har 2 haftada", "Murakkab o'g'it NPK 15-15-15"),
        ],
        "organic": "Kompost 15-20 t/ga, gumus",
    },
    "Kartoshka": {
        "N": 120, "P": 80, "K": 150,
        "schedule": [
            ("Ekishdan oldin", "Superfosfat 250 kg/ga"),
            ("Mo'l ko'karish", "Ammoniy selitra 150 kg/ga"),
            ("Gullash", "Kaliy sulfat 100 kg/ga"),
        ],
        "organic": "Chirigan go'ng 30-40 t/ga",
    },
}

DEFAULT_NORM = {
    "N": 150, "P": 90, "K": 90,
    "schedule": [
        ("Ekishdan oldin", "Superfosfat 200 kg/ga, Kaliy 100 kg/ga"),
        ("O'sish davri", "Ammoniy selitra 150 kg/ga"),
        ("Hosil berish", "Murakkab o'g'it NPK"),
    ],
    "organic": "Chirigan go'ng 20-25 t/ga",
}


@router.callback_query(F.data == "menu:fertilizer")
async def fertilizer_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "🧪 <b>O'g'itlash Tavsiyasi</b>\n\n"
        "Ekin turini tanlang — AI sizga aniq\n"
        "o'g'itlash rejasini tayyorlaydi:\n\n"
        "  📊 Qancha o'g'it kerak (NPK)\n"
        "  📅 Qachon solish kerak\n"
        "  🌿 Organik variant\n\n"
        "👇 Ekin turini tanlang:",
        reply_markup=ekin_keyboard("fert_crop"),
        parse_mode="HTML",
    )
    await state.set_state(FertilizerStates.waiting_crop)
    await callback.answer()


@router.callback_query(FertilizerStates.waiting_crop, F.data.startswith("fert_crop:"))
async def process_fert_crop(callback: CallbackQuery, state: FSMContext):
    idx = int(callback.data.split(":")[1])
    crop_full = EKIN_TURLARI[idx]
    crop_name = crop_full.split(" ", 1)[1] if " " in crop_full else crop_full

    norm = FERTILIZER_NORMS.get(crop_name, DEFAULT_NORM)

    msg = f"🧪 <b>O'g'itlash Rejasi — {crop_full}</b>\n"
    msg += "━" * 30 + "\n\n"
    msg += f"📊 <b>Yillik NPK me'yori (kg/ga):</b>\n"
    msg += f"  🟢 Azot (N):  <b>{norm['N']} kg/ga</b>\n"
    msg += f"  🔵 Fosfor (P): <b>{norm['P']} kg/ga</b>\n"
    msg += f"  🟡 Kaliy (K):  <b>{norm['K']} kg/ga</b>\n\n"

    msg += f"📅 <b>O'g'itlash jadvali:</b>\n"
    for period, desc in norm["schedule"]:
        msg += f"  📌 <b>{period}:</b>\n"
        msg += f"     {desc}\n"

    msg += f"\n🌿 <b>Organik alternativa:</b>\n"
    msg += f"  {norm['organic']}\n\n"

    msg += f"💡 <b>Muhim maslahatlar:</b>\n"
    msg += f"  • O'g'itni sug'orishdan oldin soling\n"
    msg += f"  • Ertalab yoki kechqurun soling\n"
    msg += f"  • Tuproq tahliliga asoslanib miqdorni tuzating\n"
    msg += f"  • Organik + mineral aralashma eng samarali\n"
    msg += f"  • Har 2-3 yilda tuproq tahlili qiling\n\n"

    msg += f"💰 <b>Taxminiy xarajat:</b>\n"
    cost = round((norm['N'] * 8 + norm['P'] * 6 + norm['K'] * 7) * 12.8)
    msg += f"  Mineral o'g'itlar: ~{cost:,} so'm/ga\n"
    msg += "\n" + "━" * 30 + "\n"
    msg += "🤖 <i>Aniq tavsiya uchun tuproq tahlili qiling</i>"

    try:
        async with async_session() as session:
            user_result = await session.execute(
                select(User).where(User.telegram_id == callback.from_user.id)
            )
            user = user_result.scalar_one_or_none()
            if user:
                c = Consultation(user_id=user.id, consultation_type="fertilizer",
                                 question=crop_name, answer=f"NPK: {norm['N']}-{norm['P']}-{norm['K']}")
                session.add(c)
                await session.commit()
    except Exception:
        pass

    await state.clear()
    await callback.message.edit_text(msg, parse_mode="HTML")
    await callback.message.answer("📌 Menyuga qaytish:", reply_markup=main_menu_keyboard())
    await callback.answer()
