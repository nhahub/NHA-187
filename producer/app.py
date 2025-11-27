import streamlit as st
from kafka import KafkaProducer
import json
from datetime import datetime
import uuid
import re

st.set_page_config(page_title="نظام الشكاوى الذكي", page_icon="📢", layout="centered")
st.title("نظام الشكاوى الذكي")
st.write("من فضلك املأ البيانات التالية لإرسال شكواك:")

# إعداد Kafka Producer
# Ensure 'kafka:9092' matches your Docker service name
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# === FIX: Using st.form to clear inputs after submission ===
with st.form(key='complaint_form', clear_on_submit=True):
    name = st.text_input("الاسم")
    national_id = st.text_input("الرقم القومي (14 رقم)")
    complaint = st.text_area("نص الشكوى", max_chars=500)
    
    # Must use st.form_submit_button inside a form
    submit_button = st.form_submit_button(label="إرسال الشكوى")

# عند الضغط على زر الإرسال
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
        st.error("نص الشكوى طويل جدًا، يرجى اختصاره إلى 500 حرف أو أقل.")
    else:
        complaint_data = {
            "complaint_id": str(uuid.uuid4()),          # معرف فريد لكل شكوى
            "name": name,
            "national_id": national_id,
            "complaint": complaint,
            "submitted_at": datetime.now().isoformat() # تاريخ ووقت الإرسال
        }

        # إرسال البيانات لكافكا
        producer.send("smart-complaints", value=complaint_data)

        st.success("تم إرسال الشكوى بنجاح!")
        st.info(f"معرف الشكوى: {complaint_data['complaint_id']}")