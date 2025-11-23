import pandas as pd
import random
import numpy as np
from datetime import datetime, timedelta

# 1. Configuration
num_samples = 1000
output_filename = "complaints_dataset.csv"

# 2. Vocabulary
categories = {
    'CARD_ISSUE': [
        "البطاقة ضاعت", "نسيت الرقم السري", "البطاقة مش شغالة", "عايز أعمل بدل فاقد",
        "البطاقة اتكسرت", "تحديث بيانات البطاقة", "البطاقة موقوفة", "مش عارف اصرف بالبطاقة"
    ],
    'STORE_AVAILABILITY': [
        "الزيت مش موجود", "السكر ناقص", "مفيش رز", "الجمعية فاضية",
        "السلع التموينية ناقصة", "مش لاقي مكرونة", "التجار بيخبوا البضاعة", "الأسعار غالية والسلع مش موجودة"
    ],
    'SYSTEM_DOWN': [
        "السيستم واقع", "مش عارف أدخل على الموقع", "التطبيق مهنج", "الشبكة وحشة",
        "الماكينة مش بتقرأ البطاقة", "الموقع مش بيحمل", "رسالة خطأ في التطبيق", "الخدمة غير متاحة"
    ],
    'STAFF_BEHAVIOR': [
        "الموظف زعق لي", "معاملة سيئة من الموظفين", "الموظفين مش موجودين في مكاتبهم", "رفضوا يساعدوني",
        "أسلوب الموظف غير لائق", "تعطيل مصالح الناس", "البقال بيعاملنا وحش", "الموظف رفض يسجل الشكوى"
    ],
    'BREAD_QUALITY': [
        "العيش ناشف جدا", "العيش فيه رمل", "وزن الرغيف ناقص", "العيش محروق",
        "العيش طعمه وحش", "المخبز بيطلع عيش بايظ", "العيش غير مطابق للمواصفات", "حجم الرغيف صغير"
    ]
}

prefixes = [
    "لو سمحت", "عندي مشكلة ان", "بشتكي من", "يا فندم", "حرام عليكم", "", "", "",
    "للأسف", "كنت عايز أقول", "واجهت مشكلة وهي", "أنا مواطن وبشتكي ان"
]

suffixes = [
    "ياريت تحلوا المشكلة", "حسبي الله ونعم الوكيل", "أرجو الرد بسرعة", "وده بيحصل كل يوم",
    "وشكرا", "", "", "", "الموضوع ده اتكرر كتير", "مش عارف أعمل إيه"
]

# 3. Data Generation Loop
data = []
start_date = datetime(2025, 11, 1, 0, 0)

print("Generating data...")
for i in range(num_samples):
    # Select Category & Base Text
    cat = random.choice(list(categories.keys()))
    base_text = random.choice(categories[cat])
    
    # Construct full text
    prefix = random.choice(prefixes)
    suffix = random.choice(suffixes)
    text_parts = [p for p in [prefix, base_text, suffix] if p]
    full_text = " ".join(text_parts)
    
    # Generate Sentiment (Negative/Neutral for complaints)
    sentiment = round(np.random.uniform(-0.9, -0.1), 2)
    
    # Generate Timestamp
    timestamp = (start_date + timedelta(minutes=i)).strftime('%Y-%m-%d %H:%M')
    
    data.append({
        'id': i + 1,
        'text': full_text,
        'categories': str([cat]), 
        'sentiment': sentiment,
        'timestamp': timestamp
    })

# 4. Save to CSV
df = pd.DataFrame(data)
df.to_csv(output_filename, index=False, encoding='utf-8-sig')

print(f"Success! '{output_filename}' has been created with {len(df)} rows.")