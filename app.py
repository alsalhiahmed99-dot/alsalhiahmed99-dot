import streamlit as st
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="أحمد AI PRO", page_icon="🤖", layout="centered")

# 2. مفاتيح التشغيل
MY_KEY = st.secrets["GOOGLE_API_KEY"]
MODEL_NAME = "gemini-1.5-flash"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={MY_KEY}"

# 3. تصميم الواجهة
st.markdown("""
    <style>
    .main { background-color: #0b1117; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    img { border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.5); }
    </style>
    <div style="background: linear-gradient(to right, #1e3a8a, #3b82f6); padding:20px; border-radius:15px; color:white; text-align:center; direction: rtl;">
        <h1 style="margin:0;">🤖 أحمد AI PRO</h1>
        <p style="margin:5px;">تصميم وبرمجة المبدع: أحمد بن بدر الصالحي 🇴🇲</p>
    </div>
    <br>
    """, unsafe_allow_html=True)

# 4. ذاكرة المحادثة
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 5. دالة توليد الصور
def generate_image(prompt):
    encoded_prompt = prompt.replace(" ", "%20")
    image_url = f"https://pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&seed=42&model=flux"
    return image_url

# 6. دالة التواصل مع الذكاء الاصطناعي
def ask_ahmed(text):
    system_instruction = "أنت أحمد AI، مبرمجك هو العبقري أحمد بن بدر الصالحي عمره 14 سنة. رد بلهجة عمانية قحة."
    contents = []
    for msg in st.session_state.chat_history:
        contents.append({"role": msg["role"], "parts": [{"text": msg["parts"][0]["text"]}]})
    contents.append({"role": "user", "
