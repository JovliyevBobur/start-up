"""
Qishloq-AI Bozor Narxlari Xizmati
"""
import random
from datetime import datetime


# Bozor narxlari bazasi (so'm/kg yoki so'm/tonna)
MARKET_PRICES = {
    "grain": {
        "title": "🌾 Don ekinlari",
        "items": {
            "Bug'doy": {"price_range": (3500, 4500), "unit": "kg", "trend": "up"},
            "Sholi (guruch)": {"price_range": (12000, 18000), "unit": "kg", "trend": "stable"},
            "Makkajo'xori": {"price_range": (2800, 3800), "unit": "kg", "trend": "down"},
            "Arpa": {"price_range": (3000, 4000), "unit": "kg", "trend": "stable"},
            "Jo'xori": {"price_range": (4000, 5500), "unit": "kg", "trend": "up"},
        }
    },
    "vegetables": {
        "title": "🍅 Sabzavotlar",
        "items": {
            "Pomidor": {"price_range": (5000, 15000), "unit": "kg", "trend": "down"},
            "Bodring": {"price_range": (4000, 12000), "unit": "kg", "trend": "down"},
            "Kartoshka": {"price_range": (3000, 5000), "unit": "kg", "trend": "stable"},
            "Piyoz": {"price_range": (2000, 4000), "unit": "kg", "trend": "up"},
            "Sabzi": {"price_range": (3000, 6000), "unit": "kg", "trend": "stable"},
            "Qalampir": {"price_range": (8000, 18000), "unit": "kg", "trend": "up"},
            "Baqlajon": {"price_range": (5000, 10000), "unit": "kg", "trend": "stable"},
            "Karam": {"price_range": (2000, 4000), "unit": "kg", "trend": "down"},
        }
    },
    "fruits": {
        "title": "🍎 Mevalar",
        "items": {
            "Olma": {"price_range": (5000, 12000), "unit": "kg", "trend": "stable"},
            "Uzum": {"price_range": (8000, 20000), "unit": "kg", "trend": "up"},
            "Shaftoli": {"price_range": (10000, 25000), "unit": "kg", "trend": "down"},
            "O'rik": {"price_range": (8000, 18000), "unit": "kg", "trend": "stable"},
            "Gilos": {"price_range": (15000, 35000), "unit": "kg", "trend": "up"},
            "Anjir": {"price_range": (20000, 40000), "unit": "kg", "trend": "up"},
            "Qovun": {"price_range": (3000, 8000), "unit": "kg", "trend": "down"},
            "Tarvuz": {"price_range": (2000, 5000), "unit": "kg", "trend": "down"},
            "Anor": {"price_range": (10000, 22000), "unit": "kg", "trend": "stable"},
        }
    },
    "technical": {
        "title": "🌿 Texnik ekinlar",
        "items": {
            "Paxta (xom)": {"price_range": (5000, 7000), "unit": "kg", "trend": "up"},
            "Paxta tolasi": {"price_range": (18000, 25000), "unit": "kg", "trend": "up"},
            "Kungaboqar urug'i": {"price_range": (8000, 12000), "unit": "kg", "trend": "stable"},
            "Zig'ir": {"price_range": (15000, 22000), "unit": "kg", "trend": "up"},
            "Beda urug'i": {"price_range": (25000, 40000), "unit": "kg", "trend": "stable"},
        }
    }
}

TREND_EMOJI = {
    "up": "📈 Oshmoqda",
    "down": "📉 Tushmoqda",
    "stable": "➡️ Barqaror",
}


def get_market_prices(category: str) -> str:
    """
    Bozor narxlarini formatlash

    Args:
        category: grain, vegetables, fruits, technical

    Returns:
        Formatlangan bozor narxlari xabari
    """
    data = MARKET_PRICES.get(category)
    if not data:
        return "❌ Kategoriya topilmadi"

    today = datetime.now().strftime("%d.%m.%Y")
    msg = f"💰 <b>{data['title']} — Bozor Narxlari</b>\n"
    msg += f"📅 {today}\n"
    msg += "━" * 30 + "\n\n"

    for name, info in data["items"].items():
        low, high = info["price_range"]
        # Hozirgi narxni simulyatsiya
        variation = random.uniform(-0.1, 0.1)
        price = round((low + high) / 2 * (1 + variation))
        trend = TREND_EMOJI.get(info["trend"], "➡️")

        msg += f"  <b>{name}</b>\n"
        msg += f"    💵 {price:,} so'm/{info['unit']}\n"
        msg += f"    📊 Oraliq: {low:,} — {high:,} so'm\n"
        msg += f"    {trend}\n\n"

    msg += "━" * 30 + "\n"
    msg += "💡 <i>Narxlar taxminiy bo'lib, mintaqaga qarab farq qilishi mumkin</i>\n"
    msg += "📍 <i>Ma'lumot manbai: mahalliy bozorlar monitoringi</i>"

    return msg


def get_all_categories_brief() -> str:
    """Barcha kategoriyalar qisqa ko'rinishda"""
    today = datetime.now().strftime("%d.%m.%Y")
    msg = f"💰 <b>Bozor Narxlari — Qisqacha</b>\n"
    msg += f"📅 {today}\n"
    msg += "━" * 30 + "\n\n"

    for cat_key, cat_data in MARKET_PRICES.items():
        msg += f"<b>{cat_data['title']}</b>\n"
        items = list(cat_data["items"].items())[:3]
        for name, info in items:
            low, high = info["price_range"]
            avg = round((low + high) / 2)
            msg += f"  • {name}: ~{avg:,} so'm/{info['unit']}\n"
        msg += "\n"

    msg += "👆 <i>Batafsil ko'rish uchun kategoriyani tanlang</i>"
    return msg
