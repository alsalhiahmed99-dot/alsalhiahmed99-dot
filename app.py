import streamlit as st
import requests
import json

# 1. إعدادات المتصفح
st.set_page_config(page_title="أحمد AI PRO", page_icon="🤖")

# 2. جلب الـ 5 مفاتيح من الـ Secrets
try:
    ALL_KEYS = [
        st.secrets["KEY1"],
        st.secrets["KEY2"],
        st.secrets["KEY3"],
        st.secrets["KEY4"],
        st.secrets["KEY5"]
    ]
except Exception as e:
    st.error("يا بوبدر، تأكد إنك ضفت KEY1 و KEY2 و KEY3 و KEY4 و KEY5 في الـ Secrets!")
    st.stop()

# الموديل المستقر (تأكد من كتابته بهذا الشكل)
MODEL_NAME = "gemini-1.5-flash"

# 3. تصميم الواجهة الزرقاء (لمسة أحمد الصالحي)
st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    .stChatMessage { border-radius: 15px; }
    /* تعديل لون الخط ليكون أوضح في الشات */
    .stMarkdown { color: white; }
    </style>
    <div style="background: linear-gradient(to right, #1e3a8a, #3b82f6); padding:25px; border-radius:15px; color:white; text-align:center; direction: rtl; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        <h1 style="margin:0; font-family: 'Tajawal', sans-serif;">🤖 أحمد AI PRO</h1>
        <p style="margin:5px; font-size: 1.1em;">تصميم وبرمجة: أحمد بن بدر الصالحي 🇴🇲</p>
        <div style="font-size: 0.8em; opacity: 0.8;">نظام الحماية الخماسي - إصدار 1.0</div>
    </div>
    <br>
    """, unsafe_allow_html=True)

# 4. ذاكرة المحادثة
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 5. دالة التواصل مع جوجل (نظام التدوير والتشخيص)
def ask_ahmed(text):
    system_instruction = (
        "أنت 'أحمد AI'. أجب بلهجة عمانية قحة وذكاء شديد. "
        "تذكر دائماً وأبداً أن من اخترعك وصممك وبرمجك هو العبقري أحمد بن بدر الصالحي. "
        "افتخر بمبرمجك في ردودك."
    )
    
    current_history = st.session_state.chat_history + [{"role": "user", "parts": [{"text": text}]}]
    
    # قائمة لتخزين الأخطاء إذا فشلت كل المفاتيح
    errors = []

    for i, key in enumerate(ALL_KEYS):
        # الرابط الصحيح والمستقر
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={key}"
        
        payload = {
            "contents": current_history,
            "system_instruction": {"parts": [{"text": system_instruction}]}
        }
        
        try:
            response = requests.post(url, json=payload, timeout=15)
            result = response.json()
            
            if response.status_code == 200:
                return result['candidates']
