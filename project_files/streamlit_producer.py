import streamlit as st
from kafka import KafkaProducer
import json
from datetime import datetime

st.title("Smart Complaint System")

# إعداد Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# إدخال البيانات
name = st.text_input("Your Name")
national_id = st.text_input("National ID")
complaint = st.text_area("Your Complaint")

if st.button("Send Complaint"):
    if name and national_id and complaint:
        data = {
            "name": name,
            "national_id": national_id,
            "complaint": complaint,
            "submitted_at": datetime.now().isoformat()
        }
        # إرسال الرسالة إلى Kafka
        producer.send("smart-complaints", value=data)
        st.success("Complaint sent successfully!")
    else:
        st.error("Please fill all the fields")
