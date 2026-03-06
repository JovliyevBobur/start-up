"""
Qishloq-AI Tuproq Monitoring Handler
Tuproq parametrlarini kiritish va AI tahlili
"""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy import select

from database.db import async_session
from database.models import User, SoilRecord, Consultation
from keyboards.inline import soil_params_keyboard, back_to_menu_keyboard, main_menu_keyboard
from services.soil_analysis import analyze_soil, generate_demo_soil_data
from utils.helpers import format_soil_status, get_overall_score, score_emoji

router = Router()


class SoilStates(StatesGroup):
    """Tuproq kiritish holatlari"""
    entering_params = State()
    waiting_moisture = State()
    waiting_temperature = State()
    waiting_ph = State()
    waiting_npk_n = State()
    waiting_npk_p = State()
    waiting_npk_k = State()
    waiting_ec = State()


@router.callback_query(F.data == "menu:soil")
async def soil_menu(callback: CallbackQuery, state: FSMContext):
    """Tuproq monitoring menyusi"""
    await state.clear()
    await state.set_state(SoilStates.entering_params)
    await state.update_data(
        moisture=None, temperature=None, ph=None,
        npk_n=None, npk_p=None, npk_k=None, ec=None
    )

    await callback.message.edit_text(
        "🌱 <b>Tuproq Monitoring</b>\n\n"
        "Tuproq parametrlarini kiriting — AI tahlil qilib,\n"
        "batafsil tavsiya beradi.\n\n"
        "📋 <b>Parametrlarni birma-bir kiriting:</b>\n"
        "Yoki <b>📊 Tahlil qilish</b> tugmasini bosing\n"
        "(kamida 2 ta parametr kiriting)\n\n"
        "💡 <i>Demo sinash uchun hech narsa kiritmasdan\n"
        "\"Tahlil qilish\" tugmasini bosing</i>",
        reply_markup=soil_params_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.message(Command("soil"))
async def cmd_soil(message: Message, state: FSMContext):
    """Tuproq tahlili buyrug'i"""
    await state.clear()
    await state.set_state(SoilStates.entering_params)
    await state.update_data(
        moisture=None, temperature=None, ph=None,
        npk_n=None, npk_p=None, npk_k=None, ec=None
    )

    await message.answer(
        "🌱 <b>Tuproq Monitoring</b>\n\n"
        "Tuproq parametrlarini kiriting — AI tahlil qiladi.\n\n"
        "📋 Parametrlarni birma-bir kiriting yoki\n"
        "\"📊 Tahlil qilish\" tugmasini bosing demo uchun:",
        reply_markup=soil_params_keyboard(),
        parse_mode="HTML",
    )


# ===== Parameter entry callbacks =====
@router.callback_query(F.data == "soil_param:moisture")
async def ask_moisture(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "💧 <b>Tuproq namligi (%)</b>\n\n"
        "0 dan 100 gacha raqam kiriting.\n"
        "Masalan: <b>45</b>\n\n"
        "💡 <i>O'rtacha optimal namlik: 40-60%</i>",
        parse_mode="HTML",
    )
    await state.set_state(SoilStates.waiting_moisture)
    await callback.answer()


@router.message(SoilStates.waiting_moisture)
async def process_moisture(message: Message, state: FSMContext):
    try:
        val = float(message.text.replace(",", "."))
        if not (0 <= val <= 100):
            raise ValueError()
    except ValueError:
        await message.answer("❌ Noto'g'ri. 0-100 orasida raqam kiriting:")
        return
    await state.update_data(moisture=val)
    await state.set_state(SoilStates.entering_params)
    await message.answer(
        f"✅ Namlik: <b>{val}%</b> saqlandi!\n\nKeyingi parametrni tanlang:",
        reply_markup=soil_params_keyboard(),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "soil_param:temperature")
async def ask_temperature(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "🌡 <b>Tuproq harorati (°C)</b>\n\n"
        "Raqam kiriting. Masalan: <b>25</b>\n\n"
        "💡 <i>Optimal tuproq harorati: 15-30°C</i>",
        parse_mode="HTML",
    )
    await state.set_state(SoilStates.waiting_temperature)
    await callback.answer()


@router.message(SoilStates.waiting_temperature)
async def process_temperature(message: Message, state: FSMContext):
    try:
        val = float(message.text.replace(",", "."))
        if not (-30 <= val <= 60):
            raise ValueError()
    except ValueError:
        await message.answer("❌ Noto'g'ri. -30 dan 60 gacha raqam kiriting:")
        return
    await state.update_data(temperature=val)
    await state.set_state(SoilStates.entering_params)
    await message.answer(
        f"✅ Harorat: <b>{val}°C</b> saqlandi!\n\nKeyingi parametrni tanlang:",
        reply_markup=soil_params_keyboard(),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "soil_param:ph")
async def ask_ph(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "⚗️ <b>Tuproq pH darajasi</b>\n\n"
        "0 dan 14 gacha raqam kiriting.\n"
        "Masalan: <b>6.8</b>\n\n"
        "💡 <i>Optimal pH: 6.0-7.5 (neytral)</i>",
        parse_mode="HTML",
    )
    await state.set_state(SoilStates.waiting_ph)
    await callback.answer()


@router.message(SoilStates.waiting_ph)
async def process_ph(message: Message, state: FSMContext):
    try:
        val = float(message.text.replace(",", "."))
        if not (0 <= val <= 14):
            raise ValueError()
    except ValueError:
        await message.answer("❌ Noto'g'ri. 0-14 orasida raqam kiriting:")
        return
    await state.update_data(ph=val)
    await state.set_state(SoilStates.entering_params)
    await message.answer(
        f"✅ pH: <b>{val}</b> saqlandi!\n\nKeyingi parametrni tanlang:",
        reply_markup=soil_params_keyboard(),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "soil_param:npk_n")
async def ask_npk_n(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "🧪 <b>Azot — N (mg/kg)</b>\n\n"
        "Raqam kiriting. Masalan: <b>35</b>\n\n"
        "💡 <i>Optimal azot: 20-50 mg/kg</i>",
        parse_mode="HTML",
    )
    await state.set_state(SoilStates.waiting_npk_n)
    await callback.answer()


@router.message(SoilStates.waiting_npk_n)
async def process_npk_n(message: Message, state: FSMContext):
    try:
        val = float(message.text.replace(",", "."))
        if val < 0:
            raise ValueError()
    except ValueError:
        await message.answer("❌ Noto'g'ri. Musbat raqam kiriting:")
        return
    await state.update_data(npk_n=val)
    await state.set_state(SoilStates.entering_params)
    await message.answer(
        f"✅ Azot (N): <b>{val} mg/kg</b> saqlandi!\n\nKeyingi parametrni tanlang:",
        reply_markup=soil_params_keyboard(),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "soil_param:npk_p")
async def ask_npk_p(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "🧪 <b>Fosfor — P (mg/kg)</b>\n\n"
        "Raqam kiriting. Masalan: <b>18</b>\n\n"
        "💡 <i>Optimal fosfor: 10-30 mg/kg</i>",
        parse_mode="HTML",
    )
    await state.set_state(SoilStates.waiting_npk_p)
    await callback.answer()


@router.message(SoilStates.waiting_npk_p)
async def process_npk_p(message: Message, state: FSMContext):
    try:
        val = float(message.text.replace(",", "."))
        if val < 0:
            raise ValueError()
    except ValueError:
        await message.answer("❌ Noto'g'ri. Musbat raqam kiriting:")
        return
    await state.update_data(npk_p=val)
    await state.set_state(SoilStates.entering_params)
    await message.answer(
        f"✅ Fosfor (P): <b>{val} mg/kg</b> saqlandi!\n\nKeyingi parametrni tanlang:",
        reply_markup=soil_params_keyboard(),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "soil_param:npk_k")
async def ask_npk_k(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "🧪 <b>Kaliy — K (mg/kg)</b>\n\n"
        "Raqam kiriting. Masalan: <b>25</b>\n\n"
        "💡 <i>Optimal kaliy: 15-40 mg/kg</i>",
        parse_mode="HTML",
    )
    await state.set_state(SoilStates.waiting_npk_k)
    await callback.answer()


@router.message(SoilStates.waiting_npk_k)
async def process_npk_k(message: Message, state: FSMContext):
    try:
        val = float(message.text.replace(",", "."))
        if val < 0:
            raise ValueError()
    except ValueError:
        await message.answer("❌ Noto'g'ri. Musbat raqam kiriting:")
        return
    await state.update_data(npk_k=val)
    await state.set_state(SoilStates.entering_params)
    await message.answer(
        f"✅ Kaliy (K): <b>{val} mg/kg</b> saqlandi!\n\nKeyingi parametrni tanlang:",
        reply_markup=soil_params_keyboard(),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "soil_param:ec")
async def ask_ec(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "⚡ <b>Elektr o'tkazuvchanlik — EC (mS/cm)</b>\n\n"
        "Raqam kiriting. Masalan: <b>1.5</b>\n\n"
        "💡 <i>Optimal EC: 0.5-2.0 mS/cm</i>",
        parse_mode="HTML",
    )
    await state.set_state(SoilStates.waiting_ec)
    await callback.answer()


@router.message(SoilStates.waiting_ec)
async def process_ec(message: Message, state: FSMContext):
    try:
        val = float(message.text.replace(",", "."))
        if val < 0:
            raise ValueError()
    except ValueError:
        await message.answer("❌ Noto'g'ri. Musbat raqam kiriting:")
        return
    await state.update_data(ec=val)
    await state.set_state(SoilStates.entering_params)
    await message.answer(
        f"✅ EC: <b>{val} mS/cm</b> saqlandi!\n\nKeyingi parametrni tanlang:",
        reply_markup=soil_params_keyboard(),
        parse_mode="HTML",
    )


# ===== ANALYZE =====
@router.callback_query(F.data == "soil_param:analyze")
async def analyze(callback: CallbackQuery, state: FSMContext):
    """Tuproq tahlili"""
    data = await state.get_data()

    # Agar hech narsa kiritilmagan bo'lsa, demo ma'lumot ishlatish
    all_none = all(
        data.get(k) is None
        for k in ["moisture", "temperature", "ph", "npk_n", "npk_p", "npk_k", "ec"]
    )
    if all_none:
        demo = generate_demo_soil_data()
        data.update(demo)
        demo_mode = True
    else:
        demo_mode = False

    moisture = data.get("moisture")
    temperature = data.get("temperature")
    ph = data.get("ph")
    npk_n = data.get("npk_n")
    npk_p = data.get("npk_p")
    npk_k = data.get("npk_k")
    ec = data.get("ec")

    # Tahlil
    result = analyze_soil(moisture, temperature, ph, npk_n, npk_p, npk_k, ec)
    moisture_s, ph_s, temp_s, npk_text, ec_s = format_soil_status(
        moisture, temperature, ph, npk_n, npk_p, npk_k, ec
    )
    score = get_overall_score(moisture, temperature, ph, npk_n, npk_p, npk_k, ec)
    score_e = score_emoji(score)

    # Javobni formatlash
    msg = "🌱 <b>TUPROQ TAHLILI NATIJASI</b>\n"
    if demo_mode:
        msg += "📌 <i>(Demo rejim — tasodifiy ma'lumotlar)</i>\n"
    msg += "━" * 30 + "\n\n"

    msg += f"📊 <b>Umumiy baho:</b> {score}/100 — {score_e}\n\n"

    msg += f"<b>📋 Parametrlar:</b>\n"
    if moisture is not None:
        msg += f"  💧 Namlik: {moisture}% — {moisture_s}\n"
    if temperature is not None:
        msg += f"  🌡 Harorat: {temperature}°C — {temp_s}\n"
    if ph is not None:
        msg += f"  ⚗️ pH: {ph} — {ph_s}\n"
    if npk_n is not None or npk_p is not None or npk_k is not None:
        msg += f"  🧪 NPK:\n{npk_text}"
    if ec is not None:
        msg += f"  ⚡ EC: {ec} mS/cm — {ec_s}\n"

    if result["warnings"]:
        msg += f"\n🚨 <b>Ogohlantirishlar:</b>\n"
        for w in result["warnings"]:
            msg += f"  {w}\n"

    if result["recommendations"]:
        msg += f"\n📋 <b>Tavsiyalar:</b>\n"
        for r in result["recommendations"]:
            msg += f"  • {r}\n"

    if result["actions"]:
        msg += f"\n✅ <b>Amaliy qadamlar:</b>\n"
        for a in result["actions"]:
            msg += f"  {a}\n"

    msg += "\n" + "━" * 30 + "\n"
    msg += "🤖 <i>AI tahlili — aniqroq natija uchun barcha parametrlarni kiriting</i>"

    # Bazaga saqlash
    try:
        async with async_session() as session:
            user_result = await session.execute(
                select(User).where(User.telegram_id == callback.from_user.id)
            )
            user = user_result.scalar_one_or_none()
            if user:
                soil_record = SoilRecord(
                    user_id=user.id,
                    moisture=moisture, temperature=temperature, ph=ph,
                    npk_n=npk_n, npk_p=npk_p, npk_k=npk_k, ec=ec,
                )
                session.add(soil_record)
                consultation = Consultation(
                    user_id=user.id,
                    consultation_type="soil",
                    answer=f"Score: {score}/100",
                )
                session.add(consultation)
                await session.commit()
    except Exception:
        pass

    await state.clear()
    await callback.message.edit_text(msg, parse_mode="HTML")
    await callback.message.answer(
        "📌 Yana tahlil qilish uchun menyudan tanlang:",
        reply_markup=main_menu_keyboard(),
    )
    await callback.answer()
