"""
Qishloq-AI Tuproq Tahlili Xizmati
AI asosida tuproq holati tahlili va tavsiyalar
"""
import random
from datetime import datetime


def analyze_soil(moisture=None, temperature=None, ph=None,
                 npk_n=None, npk_p=None, npk_k=None, ec=None,
                 region=None, soil_type=None):
    """
    Tuproq parametrlari asosida batafsil tahlil va tavsiyalar
    """
    recommendations = []
    warnings = []
    actions = []

    # ===== NAMLIK TAHLILI =====
    if moisture is not None:
        if moisture < 15:
            warnings.append("⚠️ OGOH BO'LING: Tuproq juda quruq!")
            actions.append("💧 Darhol sug'orish kerak — har gektarga 300-400 m³ suv")
            actions.append("🌿 Mulchalash (qoplash) tavsiya etiladi — bug'lanishni 30% kamaytiradi")
        elif moisture < 25:
            recommendations.append("Tuproq namligi past — yaqin 1-2 kun ichida sug'oring")
            actions.append("💧 Har gektarga 200-250 m³ suv bering")
        elif moisture < 40:
            recommendations.append("Tuproq namligi biroz past, lekin kritik emas")
            actions.append("💧 3-4 kun ichida sug'orishni rejalashtiring")
        elif moisture <= 70:
            recommendations.append("✅ Tuproq namligi optimal darajada — sug'orish hozircha kerak emas")
        elif moisture <= 85:
            recommendations.append("Tuproq biroz nam — sug'orishni 5-7 kunga kechiktiring")
        else:
            warnings.append("⚠️ Tuproq juda nam! Ildiz chirishi xavfi bor")
            actions.append("🚫 Sug'orishni to'xtating")
            actions.append("🔧 Drenaj tizimini tekshiring")

    # ===== pH TAHLILI =====
    if ph is not None:
        if ph < 5.0:
            warnings.append("⚠️ Tuproq juda nordon (kislotali)!")
            actions.append("�ite Ohak (CaCO₃) soling — har gektarga 3-5 tonna")
            actions.append("📅 Ohakni kuzda solish samaraliroq")
        elif ph < 5.5:
            recommendations.append("Tuproq nordon — ko'p ekinlar uchun mos emas")
            actions.append("🧪 Ohak soling — har gektarga 2-3 tonna")
        elif ph < 6.5:
            recommendations.append("Tuproq biroz nordon — aksariyat ekinlar uchun maqbul")
        elif ph <= 7.5:
            recommendations.append("✅ pH darajasi optimal — aksariyat ekinlar uchun ideal")
        elif ph <= 8.5:
            recommendations.append("Tuproq ishqoriy — temir va marganets yetishmasligi bo'lishi mumkin")
            actions.append("🧪 Oltingugurt (S) yoki ammoniy sulfat soling")
        else:
            warnings.append("⚠️ Tuproq juda ishqoriy — sho'rlanish belgilari!")
            actions.append("🧪 Gips soling — har gektarga 2-4 tonna")
            actions.append("💧 Yuvish sug'orishini amalga oshiring")

    # ===== HARORAT TAHLILI =====
    if temperature is not None:
        if temperature < 5:
            warnings.append("❄️ Tuproq harorati juda past — ekinlar o'smaydi")
            actions.append("🌿 Mulchalash yoki plyonka bilan qoplash tavsiya etiladi")
        elif temperature < 10:
            recommendations.append("Tuproq salqin — faqat sovuqbardosh ekinlar uchun mos")
            recommendations.append("🥬 Bug'doy, arpa, beda ekish mumkin")
        elif temperature < 15:
            recommendations.append("Tuproq iliq — ko'p ekinlarni ekish mumkin")
        elif temperature <= 30:
            recommendations.append("✅ Tuproq harorati optimal — barcha ekinlar uchun yaxshi")
        elif temperature <= 38:
            recommendations.append("Tuproq issiq — suv tez bug'lanadi")
            actions.append("💧 Sug'orishni ertalab (06:00-08:00) yoki kechqurun (18:00-20:00) amalga oshiring")
            actions.append("🌿 Mulchalash suv bug'lanishini 40% kamaytiradi")
        else:
            warnings.append("🔥 Tuproq juda issiq — ekin ildizlari zarar ko'rishi mumkin!")
            actions.append("💧 Zudlik bilan sovutish sug'orishi kerak")

    # ===== NPK TAHLILI =====
    if npk_n is not None:
        if npk_n < 15:
            warnings.append("⚠️ Azot (N) juda kam — ekin sarg'ayishi mumkin")
            actions.append("🧪 Karbamid (urea) soling — har gektarga 150-200 kg")
        elif npk_n < 25:
            recommendations.append("Azot biroz kam — qo'shimcha o'g'it kerak")
            actions.append("🧪 Ammoniy nitrat — har gektarga 100-150 kg")
        elif npk_n <= 50:
            recommendations.append("✅ Azot darajasi yetarli")
        else:
            warnings.append("⚠️ Azot ortiqcha — nitrat ifloslanishi xavfi!")
            actions.append("🚫 Azotli o'g'itni kamaytiring")

    if npk_p is not None:
        if npk_p < 8:
            warnings.append("⚠️ Fosfor (P) juda kam — ildiz rivojlanishi sustlashadi")
            actions.append("🧪 Superfosfat soling — har gektarga 200-300 kg")
        elif npk_p < 15:
            recommendations.append("Fosfor biroz kam")
            actions.append("🧪 Superfosfat — har gektarga 100-150 kg")
        elif npk_p <= 30:
            recommendations.append("✅ Fosfor darajasi yetarli")
        else:
            recommendations.append("Fosfor yuqori — hozircha qo'shish kerak emas")

    if npk_k is not None:
        if npk_k < 10:
            warnings.append("⚠️ Kaliy (K) juda kam — ekin stressga chidamsiz bo'ladi")
            actions.append("🧪 Kaliy xlorid soling — har gektarga 100-200 kg")
        elif npk_k < 20:
            recommendations.append("Kaliy biroz kam")
            actions.append("🧪 Kaliy sulfat — har gektarga 80-120 kg")
        elif npk_k <= 40:
            recommendations.append("✅ Kaliy darajasi yetarli")
        else:
            recommendations.append("Kaliy yuqori — hozircha qo'shish kerak emas")

    # ===== EC TAHLILI =====
    if ec is not None:
        if ec < 0.3:
            recommendations.append("EC past — mineral tarkib kam, o'g'it kerak")
        elif ec <= 2.0:
            recommendations.append("✅ EC optimal darajada")
        elif ec <= 4.0:
            warnings.append("⚠️ EC yuqori — tuproq biroz sho'rlangan")
            actions.append("💧 Yuvish sug'orishini amalga oshiring")
            actions.append("🧪 Gips soling — sho'rni kamaytirish uchun")
        else:
            warnings.append("🔴 EC juda yuqori — tuproq sho'rlangan!")
            actions.append("💧 Zudlik bilan yuvish sug'orishi kerak — 2000-3000 m³/ga")
            actions.append("🔧 Drenaj tizimini o'rnating yoki tekshiring")

    # ===== MAVSUM TAVSIYALARI =====
    month = datetime.now().month
    if month in (3, 4):
        recommendations.append("🌸 Bahor ekish mavsumi — tuproqni tayyorlang")
    elif month in (5, 6):
        recommendations.append("☀️ Sug'orish jadvalini kuchaytiring — issiq kunlar boshlanmoqda")
    elif month in (7, 8):
        recommendations.append("🔥 Eng issiq davr — sug'orishga alohida e'tibor bering")
    elif month in (9, 10):
        recommendations.append("🍂 Hosil yig'ish va kuzgi tayyorgarlik vaqti")
    elif month in (11, 12):
        recommendations.append("❄️ Qishga tayyorgarlik — tuproqni qoplang va o'g'itlang")
    else:
        recommendations.append("❄️ Qish davri — tuproq dam olish vaqti")

    return {
        "recommendations": recommendations,
        "warnings": warnings,
        "actions": actions,
    }


def generate_demo_soil_data():
    """Demo tuproq ma'lumotlarini generatsiya qilish"""
    return {
        "moisture": round(random.uniform(15, 85), 1),
        "temperature": round(random.uniform(5, 42), 1),
        "ph": round(random.uniform(4.5, 9.0), 1),
        "npk_n": round(random.uniform(5, 70), 1),
        "npk_p": round(random.uniform(3, 45), 1),
        "npk_k": round(random.uniform(5, 55), 1),
        "ec": round(random.uniform(0.1, 5.0), 2),
    }
