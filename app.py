import streamlit as st
import requests
import json
import random

# 1. إعدادات الصفحة
st.set_page_config(page_title="أحمد AI PRO", page_icon="🤖")

# 2. مفاتيح التشغيل
MY_KEY = st.secrets["GOOGLE_API_KEY"]
MODEL_NAME = "gemini-1.5-flash"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={MY_KEY}"

# 3. تصميم الواجهة (هيبة عمانية)
st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    .stChatMessage { border-radius: 15px; }
    </style>
    <div style="background: linear-gradient(to right, #1e3a8a, #3b82f6); padding:25px; border-radius:15px; color:white; text-align:center; direction: rtl;">
        <h1 style="margin:0;">🤖 أحمد AI PRO</h1>
        <p style="margin:5px;">تصميم وبرمجة: أحمد بن بدر الصالحي 🇴🇲</p>
    </div>
    <br>
    """, unsafe_allow_html=True)

# 4. ذاكرة المحادثة
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 5. دالة التواصل مع جوجل
def ask_ahmed(text):
    payload = {
        "contents": [{"role": "user", "parts": [{"text": text}]}]
    }
    try:
        response = requests.post(URL, json=payload, timeout=30)
        res_data = response.json()
        if response.status_code == 200:
            return res_data['candidates'][0]['content']['parts'][0]['text']
        else:
            error_info = res_data.get('error', {}).get('message', 'خطأ غير معروف')
            return f"السموحة يا بوبدر، جوجل يقول: {error_info}"
    except Exception as e:
        return f"فشل في الاتصال: {str(e)}"

# 6. عرض المحادثة
for message in st.session_state.chat_history:
    role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(role):
        st.write(message["parts"][0]["text"])

# 7. منطقة الإدخال والذكاء الهجين
if prompt := st.chat_input("اكتب شيئاً أو اطلب رسمة..."):
    with st.chat_message("user"):
        st.write(prompt)
    
    # فحص إذا كان الطلب صورة
    p_low = prompt.
