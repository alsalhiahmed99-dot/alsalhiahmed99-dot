import streamlit as st
import requests
import json
import random
import base64

# 1. إعدادات الصفحة
st.set_page_config(page_title="أحمد AI PRO", page_icon="🤖", layout="centered")

# 2. مفاتيح التشغيل (تأكد من وجود GOOGLE_API_KEY في Secrets)
MY_KEY = st.secrets["GOOGLE_API_KEY"]
MODEL_NAME = "gemini-1.5-flash"  # النسخة الأكثر استقراراً لضمان العمل
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={MY_KEY}"

# 3. تصميم الواجهة (هيبة عمانية)
st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    </style>
    <div style="background: linear-gradient(to right, #1e3a8a, #3b82f6); padding:20px; border-radius:15px; color:white; text-align:center; direction: rtl;">
        <h1 style="margin:0; font-family: 'Tajawal', sans-serif;">🤖 أحمد AI PRO</h1>
        <p style="margin:5px;">تصميم وبرمجة المبدع: أحمد بن بدر الصالحي 🇴🇲</p>
        <div style="font-size: 0.8em; opacity: 0.8;">إصدار الذكاء الاصطناعي 1.0 (دعم الصور الذكي)</div>
    </div>
    <br>
    """, unsafe_allow_html=True)

# 4. ذاكرة المحادثة
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 5. دالة التواصل مع جوجل (مطورة)
def ask_ahmed(text):
    is_first = len(st.session_state.chat_history) == 0
    instruction = "رحب بالعماني واذكر مبرمجك أحمد." if is_first else "أجب بلهجة عمانية قحة ورزينة."
    
    system_prompt = f"أنت ذكاء اصطناعي محترف. {instruction} مبرمجك هو أحمد بن بدر الصالحي (14 سنة)."
    
    # تجهيز الذاكرة بشكل صحيح
    contents = []
    for msg in st.session_state.chat_history:
        contents.append({"role": msg["role"], "parts": [{"text": msg["parts"][0]["text"]}]})
    contents.append({"role": "user", "parts": [{"text": text}]})
    
    payload = {
        "contents": contents,
        "system_instruction": {"parts": [{"text": system_prompt}]}
    }
    
    try:
        response = requests.post(URL, json=payload, timeout=30)
        res_json = response.json()
        if response.status_code == 200:
            return res_json['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"السموحة يا بوبدر، جوجل رد بخطأ ({response.status_code}). تأكد من الـ API Key!"
    except Exception as e:
        return "مشكلة في الشبكة، حاول مرة ثانية يا بطل!"

# 6. عرض المحادثات السابقة
for message in st.session_state.chat_history:
    role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(role):
        st.write(message["parts"][0]["text"])

# 7. منطقة الإدخال والذكاء الهجين
if prompt := st.chat_input("تحدث معي أو اطلب رسمة (مثلاً: ارسم فارس عماني)..."):
    # عرض رسالة المستخدم
    with st.chat_message("user"):
        st.write(prompt)
    
    # هل المستخدم يريد صورة؟
    if any(word in prompt.lower() for word in ["ارسم", "صورة", "image", "draw"]):
        with st.chat_message("assistant"):
            with st.spinner('أحمد AI جالس يبدع في الرسم...'):
                seed = random.randint(1, 99999)
                clean_p = prompt.replace("ارسم", "").replace("صورة", "").replace("image", "").strip()
                # رابط الصورة
                image
