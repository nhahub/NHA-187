import streamlit as st
from kafka import KafkaProducer
import json
from datetime import datetime
import uuid
import re
import time

st.set_page_config(page_title="نظام الشكاوى الذكي", page_icon="📢", layout="centered")
st.title("نظام الشكاوى الذكي")
st.write("من فضلك املأ البيانات التالية لإرسال شكواك:")

# إعداد Kafka Producer
try:
    producer = KafkaProducer(
        bootstrap_servers='kafka:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
except Exception as e:
    st.error(f"فشل الاتصال بـ Kafka: {e}")
    producer = None

# --- إعداد Session State للتحكم في الحقول ---
# تهيئة القيم إذا لم تكن موجودة
if 'name_input' not in st.session_state: st.session_state['name_input'] = ""
if 'nid_input' not in st.session_state: st.session_state['nid_input'] = ""
if 'complaint_input' not in st.session_state: st.session_state['complaint_input'] = ""

# --- نموذج الإدخال ---
with st.form(key='complaint_form', clear_on_submit=False): # جعلنا المسح يدوياً
    # لاحظ استخدام key لكل حقل
    name = st.text_input("الاسم", key="name_input")
    national_id = st.text_input("الرقم القومي (14 رقم)", key="nid_input")
    complaint = st.text_area("نص الشكوى", max_chars=500, key="complaint_input")
    
    submit_button = st.form_submit_button(label="إرسال الشكوى")

# --- المنطق عند الضغط ---
if submit_button:
    # Validation
    if not name or not national_id or not complaint:
        st.error("يرجى ملء جميع الحقول.")
    elif not re.fullmatch(r"[A-Za-z\u0600-\u06FF\s]+", name):
        st.error("الاسم يجب أن يحتوي على حروف فقط.")
    elif len(name) > 50:
        st.error("الاسم طويل جدًا، الحد الأقصى 50 حرف.")
    elif not (national_id.isdigit() and len(national_id) == 14):
        st.error("الرقم القومي يجب أن يحتوي على 14 رقم بالضبط.")
    elif len(complaint) > 500:
        st.error("نص الشكوى طويل جدًا.")
    else:
        if producer:
            complaint_data = {
                "complaint_id": str(uuid.uuid4()),
                "name": name,
                "national_id": national_id,
                "complaint": complaint,
                "submitted_at": datetime.now().isoformat()
            }

            try:
                # إرسال البيانات
                producer.send("smart-complaints", value=complaint_data)
                
                # رسالة نجاح
                st.success("تم إرسال الشكوى بنجاح!")
                st.info(f"معرف الشكوى: {complaint_data['complaint_id']}")
                
                # --- الخطوة السحرية للمسح ---
                # تفريغ القيم في الذاكرة
                st.session_state['name_input'] = ""
                st.session_state['nid_input'] = ""
                st.session_state['complaint_input'] = ""
                
                # الانتظار قليلاً ليقرأ المستخدم الرسالة ثم إعادة التحميل
                time.sleep(1.5)
                st.rerun()
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء الإرسال: {e}")