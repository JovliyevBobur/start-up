"""
Qishloq-AI Kasallik Aniqlash Xizmati (Simulyatsiya)
Rasmlar orqali ekin kasalliklarini aniqlash
"""
import random


# Ekin kasalliklari bazasi
CROP_DISEASES = [
    {
        "name": "Fuzarioz — So'lish kasalligi",
        "emoji": "🦠",
        "severity": "Yuqori",
        "symptoms": [
            "Barglar pastdan yuqoriga sarg'ayadi",
            "O'simlik so'lib boradi",
            "Ildiz va poyada qo'ng'ir dog'lar",
        ],
        "causes": "Fusarium zamburug'i — tuproqda uzoq yashaydi",
        "treatment": [
            "🧪 Fundazol 50% — 10 l suvga 10 g aralashtirib purkash",
            "🧪 Fitosporin bilan profilaktika — har 10 kunda",
            "🔄 Ekin almashlab ekish — 3-4 yil davomida",
            "🗑 Kasallangan o'simliklarni darhol olib yoqish",
        ],
        "prevention": [
            "Chidamli navlarni tanlash",
            "Urug'liklarni ekishdan oldin dorivorlash",
            "Tuproqni dezinfeksiya qilish",
        ],
    },
    {
        "name": "Un shudring (Powdery Mildew)",
        "emoji": "⚪",
        "severity": "O'rta",
        "symptoms": [
            "Barglarda oq kukun qoplami paydo bo'ladi",
            "Barglar burishadi va qurib boradi",
            "Hosildorlik kamayadi",
        ],
        "causes": "Nam va iliq havo sharoitida zamburug' tarqaladi",
        "treatment": [
            "🧪 Topaz 100 EC — 10 l suvga 2 ml",
            "🧪 Kolloid oltingugurt — 10 l suvga 30-40 g",
            "🌿 Soda eritmasi — 10 l suvga 50 g ichish sodasi + 10 g sovun",
            "💨 Havoni yaxshi aylan tirishiga e'tibor bering",
        ],
        "prevention": [
            "O'simliklar orasini keng qoldiring",
            "Sug'orishda barglarni ho'llamang",
            "Kuzda barcha qoldiqlarni yo'q qiling",
        ],
    },
    {
        "name": "Fitoftoroz (Late Blight)",
        "emoji": "🟤",
        "severity": "Juda yuqori",
        "symptoms": [
            "Barglarda qo'ng'ir-qora dog'lar",
            "Nam havoda oq mog'or paydo bo'ladi",
            "Mevalar chiriydi",
            "O'simlik tez nobud bo'ladi",
        ],
        "causes": "Phytophthora infestans zamburug'i — kartoshka va pomidorga xos",
        "treatment": [
            "🧪 Ridomil Gold — 10 l suvga 25 g",
            "🧪 Mis kuporosi (Bordeaux suyuqligi) — 1% eritma",
            "🗑 Kasallangan qismlarni darhol olib tashlang",
            "🚫 Sug'orishni kamaytiring",
        ],
        "prevention": [
            "Chidamli navlarni eking",
            "Kartoshka va pomidorni yonma-yon ekmang",
            "Yaxshi shamollatish ta'minlang",
        ],
    },
    {
        "name": "Zangla kasalligi (Rust)",
        "emoji": "🟠",
        "severity": "O'rta",
        "symptoms": [
            "Barglarda to'q sariq-qo'ng'ir dog'lar (zang rangida)",
            "Barglar vaqtidan oldin to'kiladi",
            "O'simlik sust o'sadi",
        ],
        "causes": "Puccinia zamburug'i — shamol orqali tarqaladi",
        "treatment": [
            "🧪 Tilt 250 EC — 10 l suvga 5 ml",
            "🧪 Alto Super — har 14 kunda purkash",
            "🗑 Kasallangan barglarni olib tashlang",
        ],
        "prevention": [
            "Chidamli navlarni tanlang",
            "Urug'liklarni dorivorlang",
            "Azotli o'g'itdan ortiqcha foydalanmang",
        ],
    },
    {
        "name": "Bakterial dog' kasalligi",
        "emoji": "🔵",
        "severity": "O'rta",
        "symptoms": [
            "Barglarda suvli, shaffof dog'lar",
            "Dog'lar kengayib, qo'ng'ir tusga kiradi",
            "Mevalar ham zararlanishi mumkin",
        ],
        "causes": "Xanthomonas yoki Pseudomonas bakteriyalari",
        "treatment": [
            "🧪 Mis oksixlorid — 10 l suvga 40 g",
            "🧪 Fitosporin — biologik preparat",
            "✂️ Kasallangan qismlarni kesib oling",
            "🧤 Asboblarni dezinfeksiya qiling",
        ],
        "prevention": [
            "Sog'lom urug'lik ishlatish",
            "Sug'orishda barglarni ho'llamaslik",
            "Ekin almashlab ekish",
        ],
    },
    {
        "name": "Soxta un shudring (Downy Mildew)",
        "emoji": "💜",
        "severity": "Yuqori",
        "symptoms": [
            "Barglarning yuqorisida sariq dog'lar",
            "Barglarning ostida binafsha-kulrang mog'or",
            "O'simlik o'sishdan to'xtaydi",
        ],
        "causes": "Peronospora zamburug'i — nam sharoitda tarqaladi",
        "treatment": [
            "🧪 Ridomil Gold MZ — 10 l suvga 25 g",
            "🧪 Acrobat MC — har 10-14 kunda",
            "💨 Havoni yaxshi aylantiring",
        ],
        "prevention": [
            "Nam havoda sug'orishni kamaytiring",
            "Ertalab sug'oring — barglar qurigandan keyin tun tushsin",
            "O'simliklar orasini keng qoldiring",
        ],
    },
]


def detect_disease(photo_received: bool = True) -> str:
    """
    Kasallik aniqlash (simulyatsiya)

    Haqiqiy AI model o'rniga tasodifiy kasallik tanlaydi va
    batafsil ma'lumot beradi.
    """
    if not photo_received:
        return ("📸 <b>Kasallik aniqlash uchun rasm yuboring!</b>\n\n"
                "Quyidagilarga e'tibor bering:\n"
                "• Kasallangan qismni yaqindan suring\n"
                "• Yaxshi yorug'likda suring\n"
                "• Bargning har ikki tomonini suring\n"
                "• Bir nechta rasm yuboring — aniqlik oshadi")

    # Tasodifiy kasallik tanlash
    disease = random.choice(CROP_DISEASES)
    confidence = random.randint(72, 96)

    msg = f"🔬 <b>Kasallik Aniqlash Natijasi</b>\n"
    msg += "━" * 30 + "\n\n"
    msg += f"{disease['emoji']} <b>Aniqlangan kasallik:</b>\n"
    msg += f"  <b>{disease['name']}</b>\n\n"
    msg += f"📊 <b>Aniqlik darajasi:</b> {confidence}%\n"
    msg += f"⚡ <b>Xavf darajasi:</b> {disease['severity']}\n\n"

    msg += f"🔍 <b>Belgilari:</b>\n"
    for sym in disease["symptoms"]:
        msg += f"  • {sym}\n"
    msg += f"\n🧬 <b>Sababi:</b> {disease['causes']}\n\n"

    msg += f"💊 <b>Davolash usullari:</b>\n"
    for treat in disease["treatment"]:
        msg += f"  {treat}\n"

    msg += f"\n🛡 <b>Oldini olish:</b>\n"
    for prev in disease["prevention"]:
        msg += f"  ✅ {prev}\n"

    msg += "\n" + "━" * 30 + "\n"
    msg += "⚠️ <i>Bu AI tahlili — aniq tashxis uchun agronomga murojaat qiling</i>\n"
    msg += "📞 <i>Qishloq xo'jaligi bo'limi: +998 71 239-49-18</i>"

    return msg
