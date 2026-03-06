"""
Qishloq-AI Inline Keyboards
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import VILOYATLAR, EKIN_TURLARI, TUPROQ_TURLARI


def main_menu_keyboard() -> InlineKeyboardMarkup:
    """Asosiy menyu"""
    buttons = [
        [
            InlineKeyboardButton(text="🌱 Tuproq Monitoring", callback_data="menu:soil"),
            InlineKeyboardButton(text="💧 Sug'orish Tavsiyasi", callback_data="menu:irrigation"),
        ],
        [
            InlineKeyboardButton(text="🧪 O'g'itlash Tavsiyasi", callback_data="menu:fertilizer"),
            InlineKeyboardButton(text="🌾 Ekin Tanlash", callback_data="menu:crop"),
        ],
        [
            InlineKeyboardButton(text="🔬 Kasallik Aniqlash", callback_data="menu:disease"),
            InlineKeyboardButton(text="⛅ Ob-havo", callback_data="menu:weather"),
        ],
        [
            InlineKeyboardButton(text="💰 Bozor Narxlari", callback_data="menu:market"),
            InlineKeyboardButton(text="👤 Mening Profilim", callback_data="menu:profile"),
        ],
        [
            InlineKeyboardButton(text="📊 Statistika", callback_data="menu:stats"),
            InlineKeyboardButton(text="ℹ️ Yordam", callback_data="menu:help"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def back_to_menu_keyboard() -> InlineKeyboardMarkup:
    """Menyuga qaytish tugmasi"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Asosiy Menyuga Qaytish", callback_data="menu:main")]
    ])


def viloyat_keyboard(prefix: str = "region") -> InlineKeyboardMarkup:
    """Viloyatlar ro'yxati"""
    buttons = []
    for i in range(0, len(VILOYATLAR), 2):
        row = [InlineKeyboardButton(text=VILOYATLAR[i], callback_data=f"{prefix}:{i}")]
        if i + 1 < len(VILOYATLAR):
            row.append(InlineKeyboardButton(text=VILOYATLAR[i + 1], callback_data=f"{prefix}:{i + 1}"))
        buttons.append(row)
    buttons.append([InlineKeyboardButton(text="🔙 Ortga", callback_data="menu:main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def ekin_keyboard(prefix: str = "crop") -> InlineKeyboardMarkup:
    """Ekin turlari ro'yxati"""
    buttons = []
    for i in range(0, len(EKIN_TURLARI), 2):
        row = [InlineKeyboardButton(text=EKIN_TURLARI[i], callback_data=f"{prefix}:{i}")]
        if i + 1 < len(EKIN_TURLARI):
            row.append(InlineKeyboardButton(text=EKIN_TURLARI[i + 1], callback_data=f"{prefix}:{i + 1}"))
        buttons.append(row)
    buttons.append([InlineKeyboardButton(text="🔙 Ortga", callback_data="menu:main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def tuproq_keyboard(prefix: str = "soiltype") -> InlineKeyboardMarkup:
    """Tuproq turlari ro'yxati"""
    buttons = []
    for i, soil in enumerate(TUPROQ_TURLARI):
        buttons.append([InlineKeyboardButton(text=f"🏔 {soil}", callback_data=f"{prefix}:{i}")])
    buttons.append([InlineKeyboardButton(text="🔙 Ortga", callback_data="menu:main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def confirm_keyboard(prefix: str = "confirm") -> InlineKeyboardMarkup:
    """Tasdiqlash tugmalari"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"{prefix}:yes"),
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"{prefix}:no"),
        ]
    ])


def soil_params_keyboard() -> InlineKeyboardMarkup:
    """Tuproq parametrlari kiritish"""
    buttons = [
        [InlineKeyboardButton(text="💧 Namlik (%)", callback_data="soil_param:moisture")],
        [InlineKeyboardButton(text="🌡 Harorat (°C)", callback_data="soil_param:temperature")],
        [InlineKeyboardButton(text="⚗️ pH darajasi", callback_data="soil_param:ph")],
        [InlineKeyboardButton(text="🧪 Azot — N (mg/kg)", callback_data="soil_param:npk_n")],
        [InlineKeyboardButton(text="🧪 Fosfor — P (mg/kg)", callback_data="soil_param:npk_p")],
        [InlineKeyboardButton(text="🧪 Kaliy — K (mg/kg)", callback_data="soil_param:npk_k")],
        [InlineKeyboardButton(text="⚡ Elektr o'tkazuvchanlik (mS/cm)", callback_data="soil_param:ec")],
        [
            InlineKeyboardButton(text="📊 Tahlil qilish", callback_data="soil_param:analyze"),
            InlineKeyboardButton(text="🔙 Ortga", callback_data="menu:main"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def weather_period_keyboard() -> InlineKeyboardMarkup:
    """Ob-havo davri"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📅 Bugun", callback_data="weather_period:today"),
            InlineKeyboardButton(text="📆 3 kunlik", callback_data="weather_period:3days"),
        ],
        [
            InlineKeyboardButton(text="🗓 Haftalik", callback_data="weather_period:week"),
        ],
        [InlineKeyboardButton(text="🔙 Ortga", callback_data="menu:main")],
    ])


def market_category_keyboard() -> InlineKeyboardMarkup:
    """Bozor mahsulotlari kategoriyasi"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🌾 Don ekinlari", callback_data="market_cat:grain"),
            InlineKeyboardButton(text="🍅 Sabzavotlar", callback_data="market_cat:vegetables"),
        ],
        [
            InlineKeyboardButton(text="🍎 Mevalar", callback_data="market_cat:fruits"),
            InlineKeyboardButton(text="🌿 Texnik ekinlar", callback_data="market_cat:technical"),
        ],
        [InlineKeyboardButton(text="🔙 Ortga", callback_data="menu:main")],
    ])


def profile_keyboard() -> InlineKeyboardMarkup:
    """Profil boshqaruvi"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✏️ Ismni o'zgartirish", callback_data="profile:edit_name")],
        [InlineKeyboardButton(text="📍 Viloyatni o'zgartirish", callback_data="profile:edit_region")],
        [InlineKeyboardButton(text="🏞 Yer maydonini o'zgartirish", callback_data="profile:edit_farm")],
        [InlineKeyboardButton(text="🌱 Ekin turlarini o'zgartirish", callback_data="profile:edit_crops")],
        [InlineKeyboardButton(text="📋 Maslahat tarixi", callback_data="profile:history")],
        [InlineKeyboardButton(text="🔙 Ortga", callback_data="menu:main")],
    ])


def admin_keyboard() -> InlineKeyboardMarkup:
    """Admin panel"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👥 Foydalanuvchilar soni", callback_data="admin:users_count")],
        [InlineKeyboardButton(text="📊 Statistika", callback_data="admin:statistics")],
        [InlineKeyboardButton(text="📢 Xabar yuborish (Broadcast)", callback_data="admin:broadcast")],
        [InlineKeyboardButton(text="🔙 Ortga", callback_data="menu:main")],
    ])


def irrigation_method_keyboard() -> InlineKeyboardMarkup:
    """Sug'orish usullari"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💧 Tomchilatib sug'orish", callback_data="irr_method:drip")],
        [InlineKeyboardButton(text="🌊 Egatma sug'orish", callback_data="irr_method:furrow")],
        [InlineKeyboardButton(text="🌧 Yomg'irlatib sug'orish", callback_data="irr_method:sprinkler")],
        [InlineKeyboardButton(text="🏔 Qaysi usul mos — AI taklifi", callback_data="irr_method:ai_suggest")],
        [InlineKeyboardButton(text="🔙 Ortga", callback_data="menu:main")],
    ])
