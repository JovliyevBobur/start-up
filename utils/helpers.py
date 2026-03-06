"""
Qishloq-AI Utility Helpers
"""
from datetime import datetime


def format_soil_status(moisture, temperature, ph, npk_n, npk_p, npk_k, ec):
    """Tuproq holatini formatlash"""
    # Moisture assessment
    if moisture is not None:
        if moisture < 20:
            moisture_status = "🔴 Juda quruq — darhol sug'orish kerak!"
        elif moisture < 40:
            moisture_status = "🟡 Quruqroq — sug'orish rejalashtiring"
        elif moisture < 70:
            moisture_status = "🟢 Yaxshi — optimal namlik"
        else:
            moisture_status = "🔵 Juda nam — sug'orishni to'xtating"
    else:
        moisture_status = "⚪ Ma'lumot kiritilmagan"

    # pH assessment
    if ph is not None:
        if ph < 5.5:
            ph_status = "🔴 Juda nordon — ohak kerak"
        elif ph < 6.5:
            ph_status = "🟡 Biroz nordon"
        elif ph <= 7.5:
            ph_status = "🟢 Optimal pH"
        elif ph <= 8.5:
            ph_status = "🟡 Biroz ishqoriy"
        else:
            ph_status = "🔴 Juda ishqoriy — gips kerak"
    else:
        ph_status = "⚪ Ma'lumot kiritilmagan"

    # Temperature assessment
    if temperature is not None:
        if temperature < 5:
            temp_status = "🥶 Juda sovuq — ekin o'smaydi"
        elif temperature < 15:
            temp_status = "❄️ Salqin — sovuqbardosh ekinlar uchun"
        elif temperature <= 30:
            temp_status = "🟢 Optimal harorat"
        elif temperature <= 40:
            temp_status = "🟡 Issiq — suv bug'lanishi yuqori"
        else:
            temp_status = "🔴 Juda issiq — ekin zarar ko'radi"
    else:
        temp_status = "⚪ Ma'lumot kiritilmagan"

    # NPK assessment
    npk_text = ""
    if npk_n is not None:
        if npk_n < 20:
            npk_text += "   • Azot (N): 🔴 Kam — azotli o'g'it kerak\n"
        elif npk_n <= 50:
            npk_text += "   • Azot (N): 🟢 Yetarli\n"
        else:
            npk_text += "   • Azot (N): 🟡 Yuqori — ortiqcha\n"

    if npk_p is not None:
        if npk_p < 10:
            npk_text += "   • Fosfor (P): 🔴 Kam — fosforli o'g'it kerak\n"
        elif npk_p <= 30:
            npk_text += "   • Fosfor (P): 🟢 Yetarli\n"
        else:
            npk_text += "   • Fosfor (P): 🟡 Yuqori\n"

    if npk_k is not None:
        if npk_k < 15:
            npk_text += "   • Kaliy (K): 🔴 Kam — kaliyli o'g'it kerak\n"
        elif npk_k <= 40:
            npk_text += "   • Kaliy (K): 🟢 Yetarli\n"
        else:
            npk_text += "   • Kaliy (K): 🟡 Yuqori\n"

    if not npk_text:
        npk_text = "   ⚪ Ma'lumot kiritilmagan\n"

    # EC assessment
    if ec is not None:
        if ec < 0.5:
            ec_status = "🟡 Kam mineral tarkib"
        elif ec <= 2.0:
            ec_status = "🟢 Optimal"
        elif ec <= 4.0:
            ec_status = "🟡 Biroz sho'r"
        else:
            ec_status = "🔴 Sho'rlangan — chorak kerak"
    else:
        ec_status = "⚪ Ma'lumot kiritilmagan"

    return moisture_status, ph_status, temp_status, npk_text, ec_status


def get_overall_score(moisture, temperature, ph, npk_n, npk_p, npk_k, ec):
    """Umumiy tuproq bahosi (0-100)"""
    score = 0
    count = 0

    if moisture is not None:
        count += 1
        if 40 <= moisture <= 70:
            score += 100
        elif 20 <= moisture < 40 or 70 < moisture <= 85:
            score += 60
        else:
            score += 20

    if ph is not None:
        count += 1
        if 6.0 <= ph <= 7.5:
            score += 100
        elif 5.5 <= ph < 6.0 or 7.5 < ph <= 8.0:
            score += 70
        elif 5.0 <= ph < 5.5 or 8.0 < ph <= 8.5:
            score += 40
        else:
            score += 10

    if temperature is not None:
        count += 1
        if 15 <= temperature <= 30:
            score += 100
        elif 10 <= temperature < 15 or 30 < temperature <= 35:
            score += 70
        elif 5 <= temperature < 10 or 35 < temperature <= 40:
            score += 40
        else:
            score += 10

    if npk_n is not None:
        count += 1
        if 20 <= npk_n <= 50:
            score += 100
        elif 10 <= npk_n < 20 or 50 < npk_n <= 70:
            score += 60
        else:
            score += 20

    if npk_p is not None:
        count += 1
        if 10 <= npk_p <= 30:
            score += 100
        elif 5 <= npk_p < 10 or 30 < npk_p <= 50:
            score += 60
        else:
            score += 20

    if npk_k is not None:
        count += 1
        if 15 <= npk_k <= 40:
            score += 100
        elif 8 <= npk_k < 15 or 40 < npk_k <= 60:
            score += 60
        else:
            score += 20

    if ec is not None:
        count += 1
        if 0.5 <= ec <= 2.0:
            score += 100
        elif 0.2 <= ec < 0.5 or 2.0 < ec <= 4.0:
            score += 60
        else:
            score += 20

    if count == 0:
        return 0
    return round(score / count)


def score_emoji(score):
    """Ball uchun emoji"""
    if score >= 80:
        return "🟢 A'lo"
    elif score >= 60:
        return "🟡 Yaxshi"
    elif score >= 40:
        return "🟠 O'rtacha"
    else:
        return "🔴 Yomon"


def format_number(num):
    """Sonni formatlash"""
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    return str(num)


def get_season():
    """Hozirgi fasl"""
    month = datetime.now().month
    if month in (3, 4, 5):
        return "🌸 Bahor"
    elif month in (6, 7, 8):
        return "☀️ Yoz"
    elif month in (9, 10, 11):
        return "🍂 Kuz"
    else:
        return "❄️ Qish"


def get_greeting():
    """Vaqtga qarab salomlashish"""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "🌅 Xayrli tong"
    elif 12 <= hour < 17:
        return "☀️ Xayrli kun"
    elif 17 <= hour < 22:
        return "🌆 Xayrli kech"
    else:
        return "🌙 Xayrli tun"
