"""
Qishloq-AI Start & Registration Handler
/start va /help buyruqlari, ro'yxatdan o'tish FSM
"""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy import select

from database.db import async_session
from database.models import User
from keyboards.inline import main_menu_keyboard, viloyat_keyboard, tuproq_keyboard
from keyboards.reply import phone_keyboard, remove_keyboard
from config import VILOYATLAR, TUPROQ_TURLARI, ADMIN_IDS
from utils.helpers import get_greeting

router = Router()


class RegistrationStates(StatesGroup):
    """Ro'yxatdan o'tish holatlari"""
    waiting_full_name = State()
    waiting_phone = State()
    waiting_region = State()
    waiting_farm_size = State()
    waiting_soil_type = State()


# ==================== /start ====================
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Boshlash buyrug'i"""
    await state.clear()
    telegram_id = message.from_user.id

    # Foydalanuvchi mavjudligini tekshirish
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()

    if user:
        greeting = get_greeting()
        await message.answer(
            f"{greeting}, <b>{user.full_name}</b>! 👋\n\n"
            f"🌾 <b>Qishloq-AI</b> — O'zbekiston dehqonlari uchun\n"
            f"AI tuproq maslahatchisi botiga xush kelibsiz!\n\n"
            f"📍 Viloyat: {user.region or 'Belgilanmagan'}\n"
            f"🏞 Yer maydoni: {user.farm_size or 0} ga\n\n"
            f"Quyidagi menyudan kerakli xizmatni tanlang 👇",
            reply_markup=main_menu_keyboard(),
            parse_mode="HTML",
        )
    else:
        await message.answer(
            f"🌾 <b>Qishloq-AI</b>ga xush kelibsiz! 🎉\n\n"
            f"Men sizning <b>AI tuproq maslahatchingiz</b>man.\n"
            f"Sun'iy intellekt yordamida:\n\n"
            f"  🌱 Tuproq holatini tahlil qilaman\n"
            f"  💧 Sug'orish tavsiyasi beraman\n"
            f"  🧪 O'g'itlash rejasini tuzaman\n"
            f"  🌾 Mos ekin tavsiya qilaman\n"
            f"  🔬 Kasalliklarni aniqlayman\n"
            f"  ⛅ Ob-havo ma'lumoti beraman\n"
            f"  💰 Bozor narxlarini ko'rsataman\n\n"
            f"Avval ro'yxatdan o'taylik! 📝\n"
            f"<b>Ism-familiyangizni kiriting:</b>",
            parse_mode="HTML",
        )
        await state.set_state(RegistrationStates.waiting_full_name)


# ==================== Registration FSM ====================
@router.message(RegistrationStates.waiting_full_name)
async def process_full_name(message: Message, state: FSMContext):
    """Ism-familiya qabul qilish"""
    if len(message.text) < 3:
        await message.answer("❌ Ism juda qisqa. Iltimos, to'liq ism-familiyangizni kiriting:")
        return

    await state.update_data(full_name=message.text)
    await message.answer(
        f"✅ <b>{message.text}</b>, yaxshi!\n\n"
        f"📱 Endi telefon raqamingizni ulashing yoki o'tkazib yuboring:",
        reply_markup=phone_keyboard(),
        parse_mode="HTML",
    )
    await state.set_state(RegistrationStates.waiting_phone)


@router.message(RegistrationStates.waiting_phone, F.contact)
async def process_phone_contact(message: Message, state: FSMContext):
    """Telefon raqamini kontaktdan qabul qilish"""
    await state.update_data(phone=message.contact.phone_number)
    await message.answer(
        "✅ Telefon raqam saqlandi!\n\n"
        "📍 <b>Viloyatingizni tanlang:</b>",
        reply_markup=remove_keyboard(),
        parse_mode="HTML",
    )
    await message.answer(
        "👇 Viloyatingizni tanlang:",
        reply_markup=viloyat_keyboard("reg_region"),
    )
    await state.set_state(RegistrationStates.waiting_region)


@router.message(RegistrationStates.waiting_phone, F.text == "⏭ O'tkazib yuborish")
async def process_phone_skip(message: Message, state: FSMContext):
    """Telefon raqamini o'tkazib yuborish"""
    await state.update_data(phone=None)
    await message.answer(
        "📍 <b>Viloyatingizni tanlang:</b>",
        reply_markup=remove_keyboard(),
        parse_mode="HTML",
    )
    await message.answer(
        "👇 Viloyatingizni tanlang:",
        reply_markup=viloyat_keyboard("reg_region"),
    )
    await state.set_state(RegistrationStates.waiting_region)


@router.message(RegistrationStates.waiting_phone)
async def process_phone_text(message: Message, state: FSMContext):
    """Telefon raqamini matn sifatida qayta ishlash"""
    # Oddiy telefon raqam formatini tekshirish
    phone = message.text.replace(" ", "").replace("-", "").replace("+", "")
    if phone.isdigit() and len(phone) >= 9:
        await state.update_data(phone=message.text)
        await message.answer(
            "✅ Telefon raqam saqlandi!\n\n📍 <b>Viloyatingizni tanlang:</b>",
            reply_markup=remove_keyboard(),
            parse_mode="HTML",
        )
        await message.answer(
            "👇 Viloyatingizni tanlang:",
            reply_markup=viloyat_keyboard("reg_region"),
        )
        await state.set_state(RegistrationStates.waiting_region)
    else:
        await message.answer(
            "❌ Noto'g'ri format. Telefon raqamni to'g'ri kiriting yoki\n"
            "\"📱 Telefon raqamni yuborish\" tugmasini bosing:",
            reply_markup=phone_keyboard(),
        )


@router.callback_query(RegistrationStates.waiting_region, F.data.startswith("reg_region:"))
async def process_region(callback: CallbackQuery, state: FSMContext):
    """Viloyat tanlash"""
    idx = int(callback.data.split(":")[1])
    region = VILOYATLAR[idx]
    await state.update_data(region=region)

    await callback.message.edit_text(
        f"✅ Viloyat: <b>{region}</b>\n\n"
        f"🏞 <b>Yer maydoningiz necha gektar?</b>\n"
        f"Raqam kiriting (masalan: 5 yoki 10.5):",
        parse_mode="HTML",
    )
    await state.set_state(RegistrationStates.waiting_farm_size)
    await callback.answer()


@router.message(RegistrationStates.waiting_farm_size)
async def process_farm_size(message: Message, state: FSMContext):
    """Yer maydoni kiritish"""
    try:
        farm_size = float(message.text.replace(",", "."))
        if farm_size <= 0 or farm_size > 10000:
            raise ValueError("Invalid range")
    except ValueError:
        await message.answer(
            "❌ Noto'g'ri raqam. Iltimos, faqat raqam kiriting\n"
            "Masalan: <b>5</b> yoki <b>10.5</b>",
            parse_mode="HTML",
        )
        return

    await state.update_data(farm_size=farm_size)
    await message.answer(
        f"✅ Yer maydoni: <b>{farm_size} ga</b>\n\n"
        f"🏔 <b>Tuproq turingizni tanlang:</b>",
        reply_markup=tuproq_keyboard("reg_soil"),
        parse_mode="HTML",
    )
    await state.set_state(RegistrationStates.waiting_soil_type)


@router.callback_query(RegistrationStates.waiting_soil_type, F.data.startswith("reg_soil:"))
async def process_soil_type(callback: CallbackQuery, state: FSMContext):
    """Tuproq turi tanlash va ro'yxatdan o'tishni yakunlash"""
    idx = int(callback.data.split(":")[1])
    soil_type = TUPROQ_TURLARI[idx]
    await state.update_data(soil_type=soil_type)

    # Ma'lumotlarni saqlash
    data = await state.get_data()

    async with async_session() as session:
        user = User(
            telegram_id=callback.from_user.id,
            username=callback.from_user.username,
            full_name=data["full_name"],
            phone=data.get("phone"),
            region=data.get("region"),
            farm_size=data.get("farm_size"),
            soil_type=soil_type,
            is_admin=callback.from_user.id in ADMIN_IDS,
        )
        session.add(user)
        await session.commit()

    await state.clear()

    await callback.message.edit_text(
        f"🎉 <b>Tabriklaymiz, {data['full_name']}!</b>\n\n"
        f"Siz muvaffaqiyatli ro'yxatdan o'tdingiz! ✅\n\n"
        f"📋 <b>Sizning ma'lumotlaringiz:</b>\n"
        f"  👤 Ism: {data['full_name']}\n"
        f"  📍 Viloyat: {data.get('region', 'Belgilanmagan')}\n"
        f"  🏞 Yer: {data.get('farm_size', 0)} ga\n"
        f"  🏔 Tuproq: {soil_type}\n\n"
        f"Endi quyidagi xizmatlardan foydalanishingiz mumkin 👇",
        parse_mode="HTML",
    )
    await callback.message.answer(
        "🌾 <b>Asosiy Menyu</b>\n\nKerakli xizmatni tanlang:",
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer("✅ Ro'yxatdan o'tish yakunlandi!")


# ==================== /help ====================
@router.message(Command("help"))
async def cmd_help(message: Message):
    """Yordam buyrug'i"""
    await message.answer(
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
        "  🌱 Tuproq Monitoring — tuproq parametrlarini kiriting, AI tahlil qiladi\n"
        "  💧 Sug'orish Tavsiyasi — qachon va qancha sug'orish kerakligi\n"
        "  🧪 O'g'itlash — qanday o'g'it va qancha kerakligi\n"
        "  🌾 Ekin Tanlash — viloyat va tuproqqa mos ekinlar\n"
        "  🔬 Kasallik Aniqlash — rasm yuboring, AI tahlil qiladi\n"
        "  ⛅ Ob-havo — viloyatingiz ob-havo prognozi\n"
        "  💰 Bozor Narxlari — qishloq xo'jaligi mahsulotlari narxi\n\n"
        "❓ <b>Savol:</b> @QishloqAI_support\n"
        "📞 <b>Qo'ng'iroq:</b> +998 71 239-49-18",
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML",
    )
