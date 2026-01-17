import streamlit as st
import requests
import json

# 1. إعدادات المتصفح (عشان يظهر اسمك في جوجل)
st.set_page_config(page_title="أحمد AI PRO", page_icon="🤖")

# 2. مفاتيح التشغيل (جعل المفتاح سرياً)
# تأكد من إضافة المفتاح في Streamlit Secrets باسم GOOGLE_API_KEY
MY_KEY = st.secrets["GOOGLE_API_KEY"]
MODEL_NAME = "gemini-3-flash-preview"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={MY_KEY}"

# 3. تصميم الواجهة (الألوان الزرقاء اللي طلبتها)
st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    .stChatMessage { border-radius: 15px; }
    </style>
    <div style="background: linear-gradient(to right, #1e3a8a, #3b82f6); padding:25px; border-radius:15px; color:white; text-align:center; direction: rtl; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        <h1 style="margin:0; font-family: 'Tajawal', sans-serif;">🤖 أحمد AI PRO</h1>
        <p style="margin:5px; font-size: 1.1em;">تصميم وبرمجة: أحمد بن بدر الصالحي 🇴🇲</p>
        <div style="font-size: 0.8em; opacity: 0.8;">إصدار الذكاء الاصطناعي 1.0</div>
    </div>
    <br>
    """, unsafe_allow_html=True)

# 4. ذاكرة المحادثة
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 5. دالة التواصل مع جوجل
def ask_ahmed(text):
    # تعليمات النظام: حذفت "أنت أحمد AI" من البداية لتجنب تشتت النص
    system_instruction = (
        "أجب بلهجة عمانية قحة وذكاء شديد. "
        "لا تبدأ رسالتك بذكر اسمك (أحمد AI) نهائياً لتجنب لخبطة النص. "
        "تذكر دائماً وأبداً أن من اخترعك وصممك وبرمجك هو العبقري أحمد بن بدر الصالحي، "
        "وهو مبرمج مبدع عمره 14 سنة فقط. "
        "افتخر بمبرمجك وعمره وإنجازه في ثنايا كلام
