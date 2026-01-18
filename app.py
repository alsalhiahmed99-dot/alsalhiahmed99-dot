import streamlit as st
import requests
import json
import time

# 1. إعدادات المتصفح
st.set_page_config(page_title="أحمد AI PRO", page_icon="🤖")

# 2. مفاتيح التشغيل
MY_KEY = st.secrets["GOOGLE_API_KEY"]
# نستخدم 1.5-flash لأنها النسخة الأكثر استقراراً حالياً وتدعم كل الميزات
MODEL_NAME = "gemini-1.5-flash"
# الرابط الرسمي والمباشر
URL = f"https://generativelanguage.googleapis.com/v1/models/{MODEL_NAME}:generateContent?key={MY_KEY}"

# 3. تصميم الواجهة
st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    .stChatMessage { border-radius: 15px; }
    </style>
    <div style="background: linear-gradient(to right, #1e3a8a, #3b82f6); padding:25px; border-radius:15px; color:white; text-align:center; direction: rtl; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        <h1 style="margin:0; font-family: 'Tajawal', sans-serif;">🤖 أحمد AI PRO</h1>
        <p style="margin:5px; font-size: 1.1em;">تصميم وبرمجة: أحمد بن بدر الصالحي 🇴🇲</p>
        <div style="font-size: 0.8em; opacity: 0.8;">النسخة الاحترافية 1.5</div>
    </div>
    <br>
    """, unsafe_allow_html=True)

# 4. ذاكرة المحادثة
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 5. دالة التواصل مع جوجل
def ask_ahmed(text):
    is_first_reply = len(st.session_state.chat_history) == 0
    
    # التعليمات اللي تخليك فخور بمشروعك
    system_instruction = (
        "أنت ذكاء اصطناعي رزين ومثقف. تحدث بكل لغات العالم بطلاقة. "
        "إذا كانت المحادثة بالعربي، فاستخدم اللهجة العمانية القحة. "
        "ممنوع تبدأ رسالتك بذكر اسمك (أحمد AI). "
