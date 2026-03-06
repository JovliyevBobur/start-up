"""
Qishloq-AI Bot Configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Bot
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]

# Weather API (OpenWeatherMap)
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")

# Database
DATABASE_URL = "sqlite+aiosqlite:///qishloq_ai.db"

# Throttling
THROTTLE_RATE = 0.5  # seconds between messages

# Bot info
BOT_NAME = "Qishloq-AI"
BOT_VERSION = "1.0.0"
BOT_DESCRIPTION = "🌾 O'zbekiston dehqonlari uchun AI tuproq maslahatchisi"

# Viloyatlar ro'yxati
VILOYATLAR = [
    "Toshkent viloyati",
    "Toshkent shahri",
    "Samarqand viloyati",
    "Buxoro viloyati",
    "Farg'ona viloyati",
    "Andijon viloyati",
    "Namangan viloyati",
    "Qashqadaryo viloyati",
    "Surxondaryo viloyati",
    "Jizzax viloyati",
    "Sirdaryo viloyati",
    "Navoiy viloyati",
    "Xorazm viloyati",
    "Qoraqalpog'iston Respublikasi",
]

# Ekin turlari
EKIN_TURLARI = [
    "🌾 Bug'doy",
    "🌿 Paxta",
    "🍅 Pomidor",
    "🥒 Bodring",
    "🌽 Makkajo'xori",
    "🍇 Uzum",
    "🍎 Olma",
    "🍑 Shaftoli",
    "🥔 Kartoshka",
    "🧅 Piyoz",
    "🥕 Sabzi",
    "🫑 Qalampir",
    "🍈 Qovun",
    "🍉 Tarvuz",
    "🌻 Kungaboqar",
]

# Tuproq turlari
TUPROQ_TURLARI = [
    "Qumloq tuproq",
    "Loyqa tuproq",
    "Qora tuproq (chernozem)",
    "Sho'rlangan tuproq",
    "Qo'ng'ir tuproq",
    "Bo'z tuproq",
    "Aralash tuproq",
]
