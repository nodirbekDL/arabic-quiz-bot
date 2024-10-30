import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import random

# Logging sozlamalari
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot tokeni
TOKEN = "7507539683:AAGPtUDd61_j1jF-oKw7x9vDidB7Bdk42oU"

# So'zlar bazasi
VOCAB_DATABASE = {
    1: [  # 1-dars | هَذَا
        {"uzbek": "bu", "arabic": "هَذَا"},
        {"uzbek": "uy", "arabic": "بَيْتٌ"},
        {"uzbek": "masjid", "arabic": "مَسْجِدٌ"},
        {"uzbek": "eshik", "arabic": "بَابٌ"},
        {"uzbek": "kitob", "arabic": "كِتَابٌ"},
        {"uzbek": "qalam", "arabic": "قَلَمٌ"},
        {"uzbek": "kalit", "arabic": "مِفْتَاحٌ"},
        {"uzbek": "yozuv stoli", "arabic": "مَكْتَبٌ"},
        {"uzbek": "yotoq", "arabic": "سَرِيرٌ"},
        {"uzbek": "stul", "arabic": "كُرْسِيٌّ"},
        {"uzbek": "nima", "arabic": "مَا"},
        {"uzbek": "ko'ylak", "arabic": "قَمِيصٌ"},
        {"uzbek": "yulduz", "arabic": "نَجْمٌ"},
        {"uzbek": "mi? (qo'shimcha)", "arabic": "أَ"},
        {"uzbek": "kim", "arabic": "مَنْ"},
        {"uzbek": "doktor", "arabic": "طَبِيبٌ"},
        {"uzbek": "bola", "arabic": "وَلَدٌ"},
        {"uzbek": "talaba", "arabic": "طَالِبٌ"},
        {"uzbek": "kishi", "arabic": "رَجُلٌ"},
        {"uzbek": "tijoratchi", "arabic": "تَاجِرٌ"},
        {"uzbek": "it", "arabic": "كَلْبٌ"},
        {"uzbek": "mushuk", "arabic": "قِطٌّ"},
        {"uzbek": "eshak", "arabic": "حِمَارٌ"},
        {"uzbek": "ot", "arabic": "حِصَانٌ"},
        {"uzbek": "tuya", "arabic": "جَمَلٌ"},
        {"uzbek": "xo'roz", "arabic": "دِيكٌ"},
        {"uzbek": "o'qituvchi", "arabic": "مُدَرِّسٌ"},
        {"uzbek": "ro'molcha", "arabic": "مِنْدِيلٌ"}
    ],
    
    2: [  # 2-dars | ذلك
        {"uzbek": "imom", "arabic": "إِمَامٌ"},
        {"uzbek": "tosh", "arabic": "حَجَرٌ"},
        {"uzbek": "shakar", "arabic": "سُكَّرٌ"},
        {"uzbek": "sut", "arabic": "لَبَنٌ"}
    ],
    
    3: [  # 3-dars | Aniqlik alif lomi
        {"uzbek": "oy", "arabic": "الْقَمَرُ"},
        {"uzbek": "yangi", "arabic": "جَدِيدٌ"},
        {"uzbek": "eski", "arabic": "قَدِيمٌ"},
        {"uzbek": "kir", "arabic": "وَسِخٌ"},
        {"uzbek": "toza", "arabic": "نَظِيفٌ"},
        {"uzbek": "issiq", "arabic": "حَارٌّ"},
        {"uzbek": "sovuq", "arabic": "بَارّدٌ"},
        {"uzbek": "kichkina", "arabic": "صَغِيرٌ"},
        {"uzbek": "katta", "arabic": "كَبِيرٌ"},
        {"uzbek": "ochiq", "arabic": "مَفْتُوحٌ"},
        {"uzbek": "singan", "arabic": "مَكْسُورٌ"},
        {"uzbek": "og'ir", "arabic": "ثَقِيلٌ"},
        {"uzbek": "yengil", "arabic": "خَفِيفٌ"},
        {"uzbek": "chiroyli", "arabic": "جَمِيلٌ"},
        {"uzbek": "turibdi", "arabic": "وَاقِفٌ"},
        {"uzbek": "o'tiribdi", "arabic": "جَالِسٌ"},
        {"uzbek": "shirin", "arabic": "حُلْوٌ"},
        {"uzbek": "kasal", "arabic": "مَرِيضٌ"},
        {"uzbek": "do'kon", "arabic": "الدُّكَّانُ"},
        {"uzbek": "boy", "arabic": "غَنِيٌّ"},
        {"uzbek": "uzun", "arabic": "طَوِيلٌ"},
        {"uzbek": "kambag'al", "arabic": "فَقِيرٌ"},
        {"uzbek": "kalta", "arabic": "قَصِيرٌ"},
        {"uzbek": "olma", "arabic": "التُّفَّاحُ"}
    ],
    4: [  # 4-dars | من va إلى
        {"uzbek": "maktab", "arabic": "المَدْرَسَةُ"},
        {"uzbek": "sinf", "arabic": "الفَصْلُ"},
        {"uzbek": "hammom", "arabic": "الحَمَّامُ"},
        {"uzbek": "hojatxona", "arabic": "المِرْحَاضُ"},
        {"uzbek": "oshxona", "arabic": "المَطْبَخُ"},
        {"uzbek": "xona", "arabic": "الغُرْفَةُ"},
        {"uzbek": "universitet", "arabic": "الجَامِعَةُ"},
        {"uzbek": "bozor", "arabic": "السُّوقُ"},
        {"uzbek": "Yaponiya", "arabic": "اليَابَانُ"},
        {"uzbek": "Xitoy", "arabic": "الصِّينُ"},
        {"uzbek": "Hindiston", "arabic": "الهِنْدُ"},
        {"uzbek": "Filippin", "arabic": "الفِلِبِّينُ"},
        {"uzbek": "direktor", "arabic": "المُدِيرُ"},
        {"uzbek": "ketdi", "arabic": "ذَهَبَ"},
        {"uzbek": "chiqdi", "arabic": "خَرَجَ"}
    ],

    5: [  # 5-dars | Izofa
        {"uzbek": "payg'ambar", "arabic": "الرَّسُولُ"},
        {"uzbek": "Ka'ba", "arabic": "الكَعْبَةُ"},
        {"uzbek": "ism", "arabic": "الاِسْمُ"},
        {"uzbek": "o'g'il", "arabic": "الاِبْنُ"},
        {"uzbek": "amaki", "arabic": "العَمُّ"},
        {"uzbek": "tog'a", "arabic": "الْخَالُ"},
        {"uzbek": "sumka", "arabic": "الْحَقِيبَةُ"},
        {"uzbek": "mashina", "arabic": "السَّيَّارَةُ"},
        {"uzbek": "ko'cha", "arabic": "الشَّارِعُ"},
        {"uzbek": "yopiq", "arabic": "مُغْلَقٌ"},
        {"uzbek": "tagida", "arabic": "تَحْتَ"},
        {"uzbek": "ana u yerda", "arabic": "هُنَاكَ"}
    ],

    6: [  # 6-dars | هذه
        {"uzbek": "dazmol", "arabic": "الْمِكْوَاةُ"},
        {"uzbek": "velosiped", "arabic": "الدَّرَّاجَةُ"},
        {"uzbek": "qoshiq", "arabic": "الْمِلْعَقَةُ"},
        {"uzbek": "qozon", "arabic": "الْقِدْرُ"},
        {"uzbek": "sigir", "arabic": "الْبَقَرَةُ"},
        {"uzbek": "dehqon", "arabic": "الْفَلَّاحُ"},
        {"uzbek": "burun", "arabic": "الْأَنْفُ"},
        {"uzbek": "og'iz", "arabic": "الْفَمُ"},
        {"uzbek": "quloq", "arabic": "الْأُذُنُ"},
        {"uzbek": "qo'l", "arabic": "الْيَدُ"},
        {"uzbek": "oyoq", "arabic": "الرِّجْلُ"},
        {"uzbek": "choy", "arabic": "الشَّايُ"},
        {"uzbek": "ona", "arabic": "الأُمُّ"},
        {"uzbek": "muzlatkich", "arabic": "الثَّلَّاجَةُ"},
        {"uzbek": "qahva", "arabic": "الْقَهْوَةُ"},
        {"uzbek": "tez", "arabic": "سَرِيعٌ"},
        {"uzbek": "deraza", "arabic": "النَّافِذَةُ"},
        {"uzbek": "juda", "arabic": "جِدًّا"}
    ],

    7: [  # 7-dars | تلك
        {"uzbek": "hamshira", "arabic": "الْمُمَرِّضَةُ"},
        {"uzbek": "bog'", "arabic": "الْحَدِيقَةُ"},
        {"uzbek": "o'rdak", "arabic": "الْبَطَّةُ"},
        {"uzbek": "muazzin", "arabic": "الْمُؤَذِّنُ"},
        {"uzbek": "urg'ochi tuya", "arabic": "النَّاقَةُ"},
        {"uzbek": "tuxum", "arabic": "الْبَيْضَةُ"}
    ],

    8: [  # 8-dars | Badal
        {"uzbek": "shifoxona", "arabic": "الْمُسْتَشْفَى"},
        {"uzbek": "Germaniya", "arabic": "أَلْمَانِيَا"},
        {"uzbek": "Angliya", "arabic": "إنْكَلْتَرَّ"},
        {"uzbek": "Shvetsariya", "arabic": "سُوِيسْرَا"},
        {"uzbek": "pichoq", "arabic": "السِّكِّينُ"},
        {"uzbek": "Fransiya", "arabic": "فِرَنْسَا"},
        {"uzbek": "oldida", "arabic": "أَمَامَ"},
        {"uzbek": "orqasida", "arabic": "خَلْفَ"}
    ],

    9: [  # 9-dars | Sifat
        {"uzbek": "til", "arabic": "اللُّغَةُ"},
        {"uzbek": "mashhur", "arabic": "شَهِيرٌ"},
        {"uzbek": "shahar", "arabic": "المَدِينَةُ"},
        {"uzbek": "qush", "arabic": "الطَّائِرُ"},
        {"uzbek": "kun", "arabic": "الْيَوْمُ"},
        {"uzbek": "dangasa", "arabic": "كَسْلَانُ"},
        {"uzbek": "och (qorni)", "arabic": "جَوْعَانُ"},
        {"uzbek": "chanqagan", "arabic": "عَطْشَانُ"},
        {"uzbek": "to'la", "arabic": "مَلْآنُ"},
        {"uzbek": "g'azabli", "arabic": "غَضْبَانُ"},
        {"uzbek": "chumchuq", "arabic": "الْعُصْفُورُ"},
        {"uzbek": "bugun", "arabic": "الْيَوْمَ"}
    ],

    10: [  # 10-dars | Zamir
        {"uzbek": "sinfdosh", "arabic": "الزَّمِيلُ"},
        {"uzbek": "er (juft)", "arabic": "الزَّوْجُ"},
        {"uzbek": "bir", "arabic": "وَاحِدٌ"},
        {"uzbek": "yigit", "arabic": "فَتًى"},
        {"uzbek": "birga", "arabic": "مَعَ"},
        {"uzbek": "bola", "arabic": "الطِّفْلُ"},
        {"uzbek": "Kuvayt", "arabic": "الْكُوَيْتُ"}
    ],
    11: [],  # 11-dars | Yangi so'zlar yo'q

    12: [  # 12-dars | التي
       {"uzbek": "amaki", "arabic": "الْعَمُّ"},
       {"uzbek": "amma", "arabic": "الْعَمَّةُ"},
       {"uzbek": "tog'a", "arabic": "الْخَالُ"},
       {"uzbek": "xola", "arabic": "الْخَالَةُ"},
       {"uzbek": "janob", "arabic": "سَيِّدِي"},
       {"uzbek": "xonim", "arabic": "سَيِّدَتِي"},
       {"uzbek": "tug'ruqxona", "arabic": "مُسْتَشْفَى الْوِلَادَةِ"}
    ],

    13: [  # 13-dars | Ko'plik
       {"uzbek": "dala", "arabic": "الْحَقْلُ"},
       {"uzbek": "insonlar", "arabic": "النَّاسّ"},
       {"uzbek": "qishloq", "arabic": "الْقَرْيَةُ"},
       {"uzbek": "mehmon", "arabic": "الضَّيْفُ"},
       {"uzbek": "qariya", "arabic": "الشَّيْخُ"},
       {"uzbek": "restoran", "arabic": "الْمَطْعَمُ"},
       {"uzbek": "boshlang'ich maktab", "arabic": "الْمَدْرَسَةُ الْاِبْتِدَائِيَّةُ"},
       {"uzbek": "er", "arabic": "الزَّوْجُ"},
       {"uzbek": "xotin kishi", "arabic": "الْمَرْأَةُ"},
       {"uzbek": "yaqin", "arabic": "قَرِيبٌ"},
       {"uzbek": "zaif", "arabic": "ضَعِيفٌ"},
       {"uzbek": "ona", "arabic": "أُمٌّ"},
       {"uzbek": "ota", "arabic": "أَبٌ"},
       {"uzbek": "kuchli", "arabic": "قَوِيٌّ"},
       {"uzbek": "olim", "arabic": "عَالِمٌ"}
    ],

    14: [  # 14-dars | ذَهَبْتَمْ
       {"uzbek": "nabira", "arabic": "الحَفِيدُ"},
       {"uzbek": "fakultet", "arabic": "الكُلِّيَّةُ"},
       {"uzbek": "aka/uka", "arabic": "الأَخُ"},
       {"uzbek": "xush kelibsiz", "arabic": "أهْلًا وَسَهْلًا وَمَرْحَبًا"},
       {"uzbek": "Yunoniston", "arabic": "الْيُونَانُ"},
       {"uzbek": "nasroniy", "arabic": "نَصْرَانِيٌّ"},
       {"uzbek": "shahar", "arabic": "الْبَلَدُ"}
    ],

    15: [  # 15-dars | أَنْتُنَّ
       {"uzbek": "avval", "arabic": "قَبْلَ"},
       {"uzbek": "keyin", "arabic": "بَعْدَ"},
       {"uzbek": "qanday", "arabic": "كَيْفَ"},
       {"uzbek": "qachon", "arabic": "مَتَى"},
       {"uzbek": "hafta", "arabic": "الأُسْبُوعُ"},
       {"uzbek": "oy", "arabic": "الشَّهْرُ"},
       {"uzbek": "azon", "arabic": "الأًذًانُ"},
       {"uzbek": "namoz", "arabic": "الصًّلَاةُ"},
       {"uzbek": "qaytdi", "arabic": "رَجَعَ"},
       {"uzbek": "imtihon", "arabic": "اِخْتِبَارٌ"}
    ],

    16: [],  # 16-dars | Yangi so'zlar yo'q

    17: [  # 17-dars | G'oyri oqil
       {"uzbek": "shirkat, korxona", "arabic": "الشَرِكَةُ"},
       {"uzbek": "arzon", "arabic": "رَخِيصٌ"},
       {"uzbek": "ko'ylak", "arabic": "القَمِيصُ"}
    ],
    18: [  # 18-dars | Ikkilik
       {"uzbek": "qancha, nechta", "arabic": "كَمْ"},
       {"uzbek": "bayram", "arabic": "العِيدُ"},
       {"uzbek": "g'ildirak", "arabic": "العَجَلَةُ"},
       {"uzbek": "mahalla", "arabic": "الحَيُّ"},
       {"uzbek": "riyol", "arabic": "الرِّيَالُ"},
       {"uzbek": "rak'at", "arabic": "الرَّكْعَةُ"},
       {"uzbek": "chizg'ich", "arabic": "المِسْطَرَةُ"}
    ],
    19: [  # 19-dars | Son
       {"uzbek": "pul/narx", "arabic": "الثَّمَنُ"},
       {"uzbek": "yarim", "arabic": "نِصْفٌ"},
       {"uzbek": "riyol", "arabic": "الرِّيَالُ"},
       {"uzbek": "chaqa (mayda pul)", "arabic": "الْقِرْشُ"},
       {"uzbek": "avtobus", "arabic": "الْحَافِلَةُ"},
       {"uzbek": "yo'lovchi", "arabic": "رَاكِبٌ"},
       {"uzbek": "savol", "arabic": "السُّؤَالُ"},
       {"uzbek": "eski", "arabic": "قَدِيمٌ"},
       {"uzbek": "shahar", "arabic": "الْبَلَدُ"},
       {"uzbek": "cho'ntak", "arabic": "الْجَيْبُ"},
       {"uzbek": "Yevropa", "arabic": "أُوْرُبَّا"},
       {"uzbek": "Germaniya", "arabic": "ألْمَانِيَا"},
       {"uzbek": "Bosniya", "arabic": "بُسْنِيَا"},
       {"uzbek": "Gretsiya", "arabic": "اليُونَانُ"},
       {"uzbek": "Malayziya", "arabic": "مَاليزيَا"},
       {"uzbek": "har xil", "arabic": "مُخْتَلِفَةٌ"},
       {"uzbek": "Fransiya", "arabic": "فِرَنْسَا"}
    ],
    20: [  # 20-dars | Son (muannas)
       {"uzbek": "jurnal", "arabic": "المَجَلَّةُ"},
       {"uzbek": "Indoneziya", "arabic": "إِنْدُونِيسِيَا"},
       {"uzbek": "harf", "arabic": "الحَرْفُ"},
       {"uzbek": "so'z", "arabic": "الكَلِمَةُ"}
    ],
    21: [  # 21-dars | Takrorlash
       {"uzbek": "parta", "arabic": "المَكْتَبُ"},
       {"uzbek": "stul", "arabic": "الْكُرْسِيُّ"},
       {"uzbek": "rang", "arabic": "اللَّوْنُ"},
       {"uzbek": "qibla", "arabic": "الْقِبْلَةُ"},
       {"uzbek": "va lekin", "arabic": "وَلَكِنْ"}
    ],
    22: [  # 22-dars | G'oyri munsarif
       {"uzbek": "piyola", "arabic": "الفنجان"},
       {"uzbek": "maktab", "arabic": "المدرسة"},
       {"uzbek": "masjid", "arabic": "المسجد"},
       {"uzbek": "daqiqa", "arabic": "الدقيقة"},
       {"uzbek": "dedi", "arabic": "قال"},
       {"uzbek": "dedi (ayol kishi)", "arabic": "قالت"},
       {"uzbek": "ro'molcha", "arabic": "المنديل"},
       {"uzbek": "kalit", "arabic": "المفتاح"},
       {"uzbek": "oq", "arabic": "أَبْيَضُ"},
       {"uzbek": "qizil", "arabic": "أَحْمَرُ"},
       {"uzbek": "yashil", "arabic": "أَخْضَرُ"},
       {"uzbek": "qora", "arabic": "أَسْوَدُ"},
       {"uzbek": "ko'k", "arabic": "أَزْرَقُ"},
       {"uzbek": "sariq", "arabic": "أَصْفَرُ"}
   ]
}

# Foydalanuvchi holatlari
user_states = {}
current_questions = {}

async def start(update, context):
    """Start komandasi uchun funksiya"""
    await update.message.reply_text(
        "Assalomu alaykum! Arab tili darsligi bo'yicha test botiga xush kelibsiz!\n"
        "Test ishlashni boshlash uchun /test buyrug'ini yuboring."
    )

async def test_command(update, context):
    """Test boshlash komandasi"""
    keyboard = [
        [
            InlineKeyboardButton("🇺🇿 O'zbekcha ➡️ 🇸🇦 Arabcha", callback_data="type_uz_ar"),
            InlineKeyboardButton("🇸🇦 Arabcha ➡️ 🇺🇿 O'zbekcha", callback_data="type_ar_uz")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Test turini tanlang:",
        reply_markup=reply_markup
    )

async def handle_type_selection(update, context):
    """Test turi tanlanganda"""
    query = update.callback_query
    await query.answer()
    test_type = query.data.split('_')[1:]
    
    keyboard = []
    # Darslarni faqat bo'sh bo'lmagan darslardan ko'rsatamiz
    for lesson_num in range(1, 23):
        if lesson_num not in [11, 16] and VOCAB_DATABASE.get(lesson_num, []):  # Bo'sh darslarni o'tkazib yuborish
            keyboard.append([
                InlineKeyboardButton(
                    f"{lesson_num}-dars", 
                    callback_data=f"test_{lesson_num}_{test_type[0]}_{test_type[1]}"
                )
            ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "Qaysi darsdan test ishlashni xohlaysiz?",
        reply_markup=reply_markup
    )

async def handle_test_selection(update, context):
    """Dars tanlanganda"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    data = query.data.split('_')
    lesson = int(data[1])
    test_type = (data[2], data[3])
    
    # Tanlangan darsdagi barcha so'zlardan test tuzish
    test_words = VOCAB_DATABASE[lesson].copy()
    random.shuffle(test_words)
    
    current_questions[user_id] = {
        'words': test_words,
        'current_index': 0,
        'correct': 0,
        'test_type': test_type,
        'lesson': f"{lesson}-dars"
    }
    
    await query.message.reply_text(
        f"Test boshlandi!\n"
        f"Dars: {current_questions[user_id]['lesson']}\n"
        f"Jami savollar soni: {len(test_words)} ta\n"
        f"Har bir savolga javob berish uchun variantlardan birini tanlang."
    )
    
    await send_question(query.message, user_id)

async def send_question(message, user_id):
    """Savol yuborish"""
    test_data = current_questions[user_id]
    
    if test_data['current_index'] < len(test_data['words']):
        current_word = test_data['words'][test_data['current_index']]
        test_type = test_data['test_type']
        
        if test_type[0] == 'uz':
            question_word = current_word['uzbek']
            correct = current_word['arabic']
            all_options = [w['arabic'] for lesson_words in VOCAB_DATABASE.values() for w in lesson_words]
        else:
            question_word = current_word['arabic']
            correct = current_word['uzbek']
            all_options = [w['uzbek'] for lesson_words in VOCAB_DATABASE.values() for w in lesson_words]
        
        others = [w for w in all_options if w != correct]
        wrong_options = random.sample(others, 3)
        options = wrong_options + [correct]
        random.shuffle(options)
        
        test_data['current_correct'] = correct
        test_data['options'] = {
            'A': options[0],
            'B': options[1],
            'C': options[2],
            'D': options[3]
        }
        
        keyboard = [
            [
                InlineKeyboardButton(f"A) {options[0]}", callback_data="ans_A"),
                InlineKeyboardButton(f"B) {options[1]}", callback_data="ans_B")
            ],
            [
                InlineKeyboardButton(f"C) {options[2]}", callback_data="ans_C"),
                InlineKeyboardButton(f"D) {options[3]}", callback_data="ans_D")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await message.reply_text(
            f"📝 {test_data['current_index'] + 1}-savol "
            f"(Jami: {len(test_data['words'])})\n\n"
            f"❓ {question_word} nima degani?",
            reply_markup=reply_markup
        )
    else:
        total = len(test_data['words'])
        correct = test_data['correct']
        await message.reply_text(
            f"🏁 Test tugadi!\n\n"
            f"📊 Natijalar:\n"
            f"Dars: {test_data['lesson']}\n"
            f"Jami savollar: {total} ta\n"
            f"To'g'ri javoblar: {correct} ta\n"
            f"Foiz: {(correct/total)*100:.1f}%\n\n"
            f"🔄 Yangi test boshlash uchun /test ni bosing"
        )
        del current_questions[user_id]

async def handle_answer_button(update, context):
    """Javob tugmasi bosilganda"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    if user_id not in current_questions:
        return
    
    test_data = current_questions[user_id]
    answer = query.data.split('_')[1]
    
    if test_data['options'][answer] == test_data['current_correct']:
        test_data['correct'] += 1
        await query.message.reply_text("✅ To'g'ri!")
    else:
        correct_letter = [k for k, v in test_data['options'].items() 
                         if v == test_data['current_correct']][0]
        await query.message.reply_text(
            f"❌ Noto'g'ri!\n"
            f"To'g'ri javob: {correct_letter}) {test_data['current_correct']}"
        )
    
    test_data['current_index'] += 1
    await send_question(query.message, user_id)

def main():
    """Botni ishga tushirish"""
    try:
        print("Bot ishga tushmoqda...")
        app = Application.builder().token(TOKEN).build()
        
        # Handlerlarni qo'shamiz
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("test", test_command))
        app.add_handler(CallbackQueryHandler(handle_type_selection, pattern="^type_"))
        app.add_handler(CallbackQueryHandler(handle_test_selection, pattern="^test_"))
        app.add_handler(CallbackQueryHandler(handle_answer_button, pattern="^ans_"))
        
        print("Bot ishga tushdi!")
        app.run_polling()
        
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")

if __name__ == '__main__':
    main()