"""
Qishloq-AI Ob-havo Xizmati
"""
import random
from datetime import datetime, timedelta


# Mock ob-havo ma'lumotlari — viloyatlar uchun
WEATHER_DATA = {
    "Toshkent viloyati": {"base_temp": 18, "humidity": 45, "wind": 3.5},
    "Toshkent shahri": {"base_temp": 19, "humidity": 40, "wind": 4.0},
    "Samarqand viloyati": {"base_temp": 17, "humidity": 42, "wind": 3.0},
    "Buxoro viloyati": {"base_temp": 22, "humidity": 30, "wind": 4.5},
    "Farg'ona viloyati": {"base_temp": 18, "humidity": 50, "wind": 2.5},
    "Andijon viloyati": {"base_temp": 17, "humidity": 52, "wind": 2.8},
    "Namangan viloyati": {"base_temp": 17, "humidity": 48, "wind": 3.0},
    "Qashqadaryo viloyati": {"base_temp": 21, "humidity": 35, "wind": 3.8},
    "Surxondaryo viloyati": {"base_temp": 23, "humidity": 32, "wind": 3.2},
    "Jizzax viloyati": {"base_temp": 19, "humidity": 38, "wind": 4.0},
    "Sirdaryo viloyati": {"base_temp": 19, "humidity": 40, "wind": 3.5},
    "Navoiy viloyati": {"base_temp": 21, "humidity": 28, "wind": 5.0},
    "Xorazm viloyati": {"base_temp": 20, "humidity": 35, "wind": 4.2},
    "Qoraqalpog'iston Respublikasi": {"base_temp": 19, "humidity": 25, "wind": 5.5},
}

WEATHER_CONDITIONS = [
    ("☀️ Ochiq havo", "clear"),
    ("⛅ Qisman bulutli", "partly_cloudy"),
    ("☁️ Bulutli", "cloudy"),
    ("🌧 Yomg'irli", "rainy"),
    ("⛈ Momaqaldiroqli", "thunderstorm"),
    ("🌤 Bulutli-ochiq", "mostly_clear"),
]

AGRO_TIPS = {
    "clear": [
        "☀️ Ochiq havo — sug'orishni ertalab (06:00-08:00) yoki kechqurun (18:00-20:00) amalga oshiring",
        "🌡 Issiq kunlarda mulchalash suv bug'lanishini 30-40% kamaytiradi",
        "🌿 Ekinlarni kuzatib boring — quyosh kuyishi mumkin",
    ],
    "partly_cloudy": [
        "⛅ O'rtacha sharoit — kundalik sug'orish jadvaliga amal qiling",
        "🌱 Yangi ko'chat ekish uchun qulay havo",
    ],
    "cloudy": [
        "☁️ Bulutli havo — sug'orishni kamaytiring",
        "🧪 O'g'itlash uchun yaxshi vaqt — yomg'ir kutilmoqda",
    ],
    "rainy": [
        "🌧 Yomg'ir kutilmoqda — sug'orishni to'xtating",
        "🔧 Drenaj tizimini tekshiring",
        "⚠️ Zamburug' kasalliklari xavfi oshadi — profilaktika qiling",
    ],
    "thunderstorm": [
        "⛈ Kuchli yomg'ir va do'l xavfi — ekinlarni himoya qiling",
        "🏠 Dala ishlarini vaqtincha to'xtating",
        "⚠️ Suv toshqini xavfi — ariqlarni tozalang",
    ],
    "mostly_clear": [
        "🌤 Qulay havo — dala ishlari uchun yaxshi kun",
        "💧 Odatiy sug'orish jadvaliga amal qiling",
    ],
}


def get_seasonal_adjustment():
    """Faslga qarab harorat tuzatish"""
    month = datetime.now().month
    adjustments = {
        1: -15, 2: -10, 3: -2, 4: 5, 5: 12, 6: 18,
        7: 22, 8: 20, 9: 12, 10: 5, 11: -3, 12: -12,
    }
    return adjustments.get(month, 0)


def get_weather(region: str, days: int = 1) -> list:
    """
    Ob-havo ma'lumotlarini qaytarish

    Args:
        region: Viloyat nomi
        days: Necha kunlik prognoz (1, 3, 7)

    Returns:
        Ob-havo ma'lumotlari ro'yxati
    """
    base = WEATHER_DATA.get(region, {"base_temp": 18, "humidity": 40, "wind": 3.5})
    seasonal_adj = get_seasonal_adjustment()
    forecasts = []

    for day_offset in range(days):
        date = datetime.now() + timedelta(days=day_offset)
        condition = random.choice(WEATHER_CONDITIONS)

        # Haroratni hisoblash
        temp_variation = random.uniform(-3, 3)
        temp = round(base["base_temp"] + seasonal_adj + temp_variation, 1)
        temp_min = round(temp - random.uniform(4, 8), 1)
        temp_max = round(temp + random.uniform(3, 7), 1)

        # Namlik
        humidity = min(100, max(10, round(base["humidity"] + random.uniform(-10, 10))))

        # Shamol
        wind = round(base["wind"] + random.uniform(-1, 2), 1)

        # Yog'ingarchilik
        rain_chance = 0
        if condition[1] in ("rainy", "thunderstorm"):
            rain_chance = random.randint(60, 95)
        elif condition[1] in ("cloudy", "partly_cloudy"):
            rain_chance = random.randint(10, 40)

        # Agro maslahat
        tips = AGRO_TIPS.get(condition[1], ["📋 Kundalik rejaga amal qiling"])

        forecasts.append({
            "date": date.strftime("%d.%m.%Y"),
            "day_name": get_uzbek_day_name(date.weekday()),
            "condition": condition[0],
            "condition_type": condition[1],
            "temp": temp,
            "temp_min": temp_min,
            "temp_max": temp_max,
            "humidity": humidity,
            "wind": wind,
            "rain_chance": rain_chance,
            "tips": tips,
        })

    return forecasts


def get_uzbek_day_name(weekday: int) -> str:
    """Hafta kuni nomi"""
    days = [
        "Dushanba", "Seshanba", "Chorshanba", "Payshanba",
        "Juma", "Shanba", "Yakshanba"
    ]
    return days[weekday]


def format_weather_message(forecast: dict, region: str) -> str:
    """Ob-havo ma'lumotlarini formatlash"""
    msg = f"📍 <b>{region}</b>\n"
    msg += f"📅 <b>{forecast['day_name']}, {forecast['date']}</b>\n\n"
    msg += f"{forecast['condition']}\n\n"
    msg += f"🌡 <b>Harorat:</b> {forecast['temp']}°C\n"
    msg += f"   ↓ Min: {forecast['temp_min']}°C  |  ↑ Max: {forecast['temp_max']}°C\n"
    msg += f"💧 <b>Namlik:</b> {forecast['humidity']}%\n"
    msg += f"💨 <b>Shamol:</b> {forecast['wind']} m/s\n"

    if forecast['rain_chance'] > 0:
        msg += f"🌧 <b>Yog'in ehtimoli:</b> {forecast['rain_chance']}%\n"

    msg += f"\n🌾 <b>Dehqon uchun maslahat:</b>\n"
    for tip in forecast['tips']:
        msg += f"  {tip}\n"

    return msg
