import streamlit as st
import requests
import json

# 1. إعدادات المتصفح
st.set_page_config(page_title="أحمد AI PRO", page_icon="🤖", layout="centered")

# 2. مفاتيح التشغيل (تأكد من وجود GOOGLE_API_KEY في Streamlit Secrets)
MY_KEY = st.secrets["GOOGLE_API_KEY"]
MODEL_NAME = "gemini-1.5-flash" # تم تحديث الموديل لضمان الاستقرار
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={MY_KEY}"

# 3. تصميم الواجهة (الأزرق الملكي اللي تحبه)
st.markdown("""
    <style>
    .main { background-color: #0b1117; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    /* تنسيق الصورة لتظهر بشكل جميل */
    img { border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.5); }
    </style>
    <div style="background: linear-gradient(to right, #1e3a8a, #3b82f6); padding:25px; border-radius:15px; color:white; text-align:center; direction: rtl; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        <h1 style="margin:0; font-family: 'Tajawal', sans-serif;">🤖 أحمد AI PRO</h1>
        <p style="margin:5px; font-size: 1.1em;">تصميم وبرمجة المبدع: أحمد بن بدر الصالحي 🇴🇲</p>
        <div style="font-size: 0.8em; opacity: 0.8;">إصدار الذكاء الاصطناعي 1.1 (دعم توليد الصور)</div>
    </div>
    <br>
    """, unsafe_allow_html=True)

# 4. ذاكرة المحادثة
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 5. دالة توليد الصور (جديد)
def generate_image(prompt):
    # نستخدم محرك Pollinations السريع والمجاني
    # نقوم بإضافة "digital art" للبرومبت لضمان جودة عالية
    encoded_prompt = prompt.replace(" ", "%20")
    image_url = f"https://pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&seed=42&model=flux"
    return image_url

# 6. دالة التواصل مع
