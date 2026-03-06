"""
Qishloq-AI Ekin Tavsiya Xizmati
Tuproq turi, iqlim mintaqasi va fasl asosida ekin tavsiyalari
"""
from datetime import datetime
from config import VILOYATLAR


# Mintaqa bo'yicha ekin mosligini
REGION_CROPS = {
    "Toshkent viloyati": {
        "asosiy": ["Bug'doy", "Paxta", "Uzum", "Olma", "Pomidor", "Kartoshka"],
        "tavsiya": ["Gilos", "O'rik", "Bodring", "Qalampir"],
        "iqlim": "Mo''tadil continental",
    },
    "Farg'ona viloyati": {
        "asosiy": ["Paxta", "Uzum", "Shaftoli", "O'rik", "Pomidor"],
        "tavsiya": ["Anor", "Anjir", "Olma", "Bug'doy"],
        "iqlim": "Issiq, quruq yoz",
    },
    "Samarqand viloyati": {
        "asosiy": ["Bug'doy", "Paxta", "Uzum", "Sabzi", "Piyoz"],
        "tavsiya": ["Olma", "O'rik", "Kartoshka", "Makkajo'xori"],
        "iqlim": "Mo''tadil continental",
    },
    "Buxoro viloyati": {
        "asosiy": ["Paxta", "Bug'doy", "Qovun", "Tarvuz"],
        "tavsiya": ["Kungaboqar", "Beda", "Uzum"],
        "iqlim": "Issiq cho'l iqlimi",
    },
    "Andijon viloyati": {
        "asosiy": ["Paxta", "Bug'doy", "Uzum", "Pomidor", "Shaftoli"],
        "tavsiya": ["Gilos", "O'rik", "Bodring", "Qalampir"],
        "iqlim": "Issiq, quruq yoz",
    },
    "Namangan viloyati": {
        "asosiy": ["Paxta", "Bug'doy", "Anor", "Uzum"],
        "tavsiya": ["Pomidor", "Bodring", "O'rik", "Olma"],
        "iqlim": "Mo''tadil",
    },
    "Qashqadaryo viloyati": {
        "asosiy": ["Bug'doy", "Paxta", "Qovun", "Tarvuz"],
        "tavsiya": ["Kartoshka", "Makkajo'xori", "Kungaboqar"],
        "iqlim": "Issiq, quruq",
    },
    "Surxondaryo viloyati": {
        "asosiy": ["Paxta", "Bug'doy", "Sitrus mevalari", "Anor"],
        "tavsiya": ["Anjir", "Qovun", "Tarvuz", "Uzum"],
        "iqlim": "Subtropik, eng issiq viloyat",
    },
    "Jizzax viloyati": {
        "asosiy": ["Bug'doy", "Paxta", "Kartoshka"],
        "tavsiya": ["Sabzi", "Piyoz", "Makkajo'xori"],
        "iqlim": "Continental",
    },
    "Sirdaryo viloyati": {
        "asosiy": ["Bug'doy", "Paxta", "Sholi"],
        "tavsiya": ["Pomidor", "Bodring", "Piyoz"],
        "iqlim": "Mo''tadil continental",
    },
    "Navoiy viloyati": {
        "asosiy": ["Bug'doy", "Paxta", "Qovun"],
        "tavsiya": ["Tarvuz", "Beda", "Kungaboqar"],
        "iqlim": "Cho'l iqlimi, quruq",
    },
    "Xorazm viloyati": {
        "asosiy": ["Paxta", "Sholi", "Bug'doy", "Qovun"],
        "tavsiya": ["Tarvuz", "Piyoz", "Sabzi"],
        "iqlim": "Continental, quruq",
    },
    "Qoraqalpog'iston Respublikasi": {
        "asosiy": ["Paxta", "Sholi", "Bug'doy"],
        "tavsiya": ["Qovun", "Tarvuz", "Beda"],
        "iqlim": "Cho'l, juda quruq, Orol ta'siri",
    },
    "Toshkent shahri": {
        "asosiy": ["Pomidor", "Bodring", "Qalampir", "Gul"],
        "tavsiya": ["Issiqxona ekinlari", "Zira", "Greens"],
        "iqlim": "Shahar iqlimi",
    },
}

# Tuproq turiga mos ekinlar
SOIL_CROPS = {
    "Qumloq tuproq": {
        "mos": ["Tarvuz", "Qovun", "Kartoshka", "Sabzi", "Piyoz", "Kungaboqar"],
        "xususiyat": "Suv tez singadi, oziq moddalar yuvilib ketadi. Tez-tez sug'orish va o'g'itlash kerak.",
    },
    "Loyqa tuproq": {
        "mos": ["Bug'doy", "Sholi", "Beda", "Paxta", "Karam"],
        "xususiyat": "Suvni yaxshi ushlab turadi, lekin qotib qolishi mumkin. Haydash va yumshatish kerak.",
    },
    "Qora tuproq (chernozem)": {
        "mos": ["Bug'doy", "Makkajo'xori", "Kungaboqar", "Pomidor", "Kartoshka", "Uzum", "Olma"],
        "xususiyat": "Eng unumdor tuproq! Deyarli barcha ekinlar uchun ideal.",
    },
    "Sho'rlangan tuproq": {
        "mos": ["Beda", "Sholi", "Paxta (chidamli navlar)", "Tuzga chidamli o'tlar"],
        "xususiyat": "Sho'r tarkib ko'p ekinlarga zarar. Yuvish va gips solish kerak.",
    },
    "Qo'ng'ir tuproq": {
        "mos": ["Bug'doy", "Arpa", "Uzum", "Olma", "Beda"],
        "xususiyat": "O'rtacha unumdorlik. O'g'itlash va muntazam sug'orish bilan yaxshi hosil beradi.",
    },
    "Bo'z tuproq": {
        "mos": ["Paxta", "Bug'doy", "Qovun", "Tarvuz"],
        "xususiyat": "O'zbekistonda keng tarqalgan. Sug'orilganda unumdor.",
    },
    "Aralash tuproq": {
        "mos": ["Ko'p ekinlar mos", "Pomidor", "Bodring", "Bug'doy", "Kartoshka"],
        "xususiyat": "Qum va loy aralashmasi — suv va havo almashishi yaxshi.",
    },
}


def get_crop_recommendation(region: str = None, soil_type: str = None):
    """
    Ekin tavsiyasi berish

    Args:
        region: Viloyat nomi
        soil_type: Tuproq turi

    Returns:
        Tavsiya matni
    """
    month = datetime.now().month

    # Mavsumga qarab ekish tavsiyasi
    if month in (2, 3, 4):
        season = "🌸 Bahor"
        season_crops = ["Bug'doy (kuzgi hosilni o'rish)", "Kartoshka", "Piyoz", "Sabzi",
                        "Pomidor ko'chati", "Bodring ko'chati", "Makkajo'xori"]
        season_tip = "Bahor ekish mavsumi — tuproqni haydab, o'g'itlab tayyorlang"
    elif month in (5, 6):
        season = "☀️ Erta yoz"
        season_crops = ["Paxta", "Makkajo'xori", "Qovun", "Tarvuz",
                        "Pomidor (ikkinchi marta)", "Bodring", "Qalampir"]
        season_tip = "Issiq mavsumga mos ekinlarni eking, sug'orishni kuchaytiring"
    elif month in (7, 8):
        season = "🔥 Yoz"
        season_crops = ["Kuzgi ekinlar uchun tayyorgarlik", "Beda",
                        "Kartoshka (ikkinchi marta)", "Karam", "Sabzi (kuzgi)"]
        season_tip = "Eng issiq davr — sug'orishga e'tibor bering, kuzgi ekish uchun rejalashtiring"
    elif month in (9, 10):
        season = "🍂 Kuz"
        season_crops = ["Bug'doy (kuzgi)", "Arpa (kuzgi)", "Sarimsoq", "Piyoz (kuzgi)"]
        season_tip = "Kuzgi ekish mavsumi — bug'doy va arpa eking"
    else:
        season = "❄️ Qish"
        season_crops = ["Issiqxona ekinlari", "Pomidor (issiqxona)", "Bodring (issiqxona)"]
        season_tip = "Qish davri — issiqxonalarda ekin etishtirish, bahori tayyorgarlik"

    # Javobni shakllantirish
    msg = f"🌾 <b>Ekin Tanlash Tavsiyasi</b>\n"
    msg += f"📅 Mavsun: <b>{season}</b>\n"
    msg += "━" * 30 + "\n\n"

    # Viloyat bo'yicha tavsiya
    if region and region in REGION_CROPS:
        r = REGION_CROPS[region]
        msg += f"📍 <b>{region}</b>\n"
        msg += f"🌤 Iqlim: {r['iqlim']}\n\n"
        msg += f"✅ <b>Asosiy ekinlar:</b>\n"
        for crop in r["asosiy"]:
            msg += f"  • {crop}\n"
        msg += f"\n💡 <b>Tavsiya etiladigan ekinlar:</b>\n"
        for crop in r["tavsiya"]:
            msg += f"  • {crop}\n"
        msg += "\n"

    # Tuproq turi bo'yicha tavsiya
    if soil_type and soil_type in SOIL_CROPS:
        s = SOIL_CROPS[soil_type]
        msg += f"🏔 <b>Tuproq turi: {soil_type}</b>\n"
        msg += f"📋 {s['xususiyat']}\n\n"
        msg += f"✅ <b>Bu tuproqqa mos ekinlar:</b>\n"
        for crop in s["mos"]:
            msg += f"  • {crop}\n"
        msg += "\n"

    # Mavsumiy tavsiya
    msg += f"📆 <b>Hozirgi mavsumda ekiladigan ekinlar ({season}):</b>\n"
    for crop in season_crops:
        msg += f"  🌱 {crop}\n"
    msg += f"\n💡 <b>Maslahat:</b> {season_tip}\n"

    # Umumiy tavsiyalar
    msg += "\n" + "━" * 30 + "\n"
    msg += "📌 <b>Muhim eslatmalar:</b>\n"
    msg += "  • Ekin almashlab ekish hosildorlikni 15-20% oshiradi\n"
    msg += "  • Monoekinchilikdan saqlaning — tuproq charchaydi\n"
    msg += "  • Mahalliy nav urug'liklarini tanlang — iqlimga moslashgan\n"

    return msg
