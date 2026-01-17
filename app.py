import streamlit as st
import requests
import json

# 1. إعدادات الصفحة
st.set_page_config(page_title="أحمد AI PRO", page_icon="🤖", layout="centered")

# 2. مفاتيح التشغيل (يتم جلبها من Streamlit Secrets)
# تأكد من إضافة GOOGLE_API_KEY في إعدادات Secrets على موقع Streamlit
MY_KEY = st.secrets["GOOGLE_API_KEY"]
MODEL_NAME = "gemini-1.5-flash"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={MY_KEY}"

# 3. تصميم الواجهة (الألوان والستايل)
st.markdown("""
    <style>
    .main { background-color: #0b1117; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    img { border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.5); }
    /* ضمان ظهور مربع الإدخال بشكل صحيح */
    .stChatInput { bottom: 20px; }
    </style>
    <div style="background: linear-gradient(to right, #1e3a8a, #3b82f6); padding:25px; border-radius:15px; color:white; text-align:center; direction: rtl; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        <h1 style="margin:0; font-family: 'Tajawal', sans-serif;">🤖 أحمد AI PRO</h1>
        <p style="margin:5px; font-size: 1.1em;">تصميم وبرمجة المبدع: أحمد بن بدر الصالحي 🇴🇲</p>
        <div style="font-size: 0.8em; opacity: 0.8;">إصدار 1.1 - يدعم توليد الصور والمحادثة العمانية</div>
    </div>
    <br>
    """, unsafe_allow_html=True)

# 4. ذاكرة المحادثة
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 5. دالة توليد الصور
def generate_image(prompt):
    # محرك Pollinations السريع
    encoded_prompt = prompt.replace(" ", "%20")
    image_url = f"https://pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&seed=42&model=flux"
    return image_url

# 6. دالة التواصل مع الذكاء الاصطناعي (Gemini)
def ask_ahmed(text):
    system_instruction = (
        "أنت ذكاء اصطناعي اسمك أحمد AI. "
        "أجب بلهجة عمانية قحة وذكاء شديد. "
        "من اخترعك وصممك وبرمجك هو العبقري العماني أحمد بن بدر الصالحي، "
        "وهو مبرمج مبدع عمره 14 سنة فقط. افتخر به دائماً."
    )
    
    # تحضير الرسائل للـ API
    contents = []
    for msg in st.session_state.chat_history:
        contents.append({"role": msg["role"], "parts": [{"text": msg["parts"][0]["text"]}]})
    contents.append({"role": "user",
