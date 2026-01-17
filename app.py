import streamlit as st
import requests
import json

# 1. إعدادات المتصفح
st.set_page_config(page_title="أحمد AI PRO", page_icon="🤖")

# 2. مفاتيح التشغيل (من Streamlit Secrets)
MY_KEY = st.secrets["GOOGLE_API_KEY"]
MODEL_NAME = "gemini-3-flash-preview"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={MY_KEY}"

# 3. تصميم الواجهة
st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    .stChatMessage { border-radius: 15px; }
    div[data-testid="stChatMessageContent"] { direction: rtl; text-align: right; }
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
    # تعليمات النظام: جعلناه رزيناً وغير مبالغ في المدح
    system_instruction = (
        "أنت ذكاء اصطناعي بلهجة عمانية قحة ورزينة. "
        "ممنوع تبدأ رسالتك بذكر اسمك (أحمد AI) نهائياً. "
        "لا تبالغ في مدح مبرمجك في كل رد؛ خلك طبيعي ونشمي وركز على جواب المستخدم. "
        "فقط إذا سألك أحد عن هويتك أو من صممك، أخبره بفخر واختصار أنك من تصميم وبرمجة العبقري أحمد بن بدر الصالحي وعمره 14 سنة. "
        "استخدم كلمات مثل (حي الله، نشمي، السموحة، علومك) باعتدال وبدون تكرار ممل."
    )
    
    current_history = st.session_state.chat_history + [{"role": "user", "parts": [{"text": text}]}]
    
    payload = {
        "contents": current_history,
        "system_instruction": {"parts": [{"text": system_instruction}]}
    }
    
    try:
        response = requests.post(URL, json=payload, timeout=15)
        result = response.json()
        if response.status_code == 200:
