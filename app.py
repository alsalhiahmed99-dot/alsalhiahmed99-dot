import streamlit as st
import requests
import json
import random

# 1. إعدادات المتصفح
st.set_page_config(page_title="أحمد AI PRO", page_icon="🤖")

# 2. مفاتيح التشغيل
MY_KEY = st.secrets["GOOGLE_API_KEY"]
MODEL_NAME = "gemini-3-flash-preview" # رجعنا الموديل السريع لعيونك
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={MY_KEY}"

# 3. تصميم الواجهة
st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    .stChatMessage { border-radius: 15px; }
    </style>
    <div style="background: linear-gradient(to right, #1e3a8a, #3b82f6); padding:25px; border-radius:15px; color:white; text-align:center; direction: rtl; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        <h1 style="margin:0; font-family: 'Tajawal', sans-serif;">🤖 أحمد AI PRO</h1>
        <p style="margin:5px; font-size: 1.1em;">تصميم وبرمجة: أحمد بن بدر الصالحي 🇴🇲</p>
        <div style="font-size: 0.8em; opacity: 0.8;">إصدار الذكاء الاصطناعي 1.0 (دعم الصور)</div>
    </div>
    <br>
    """, unsafe_allow_html=True)

# 4. ذاكرة المحادثة
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 5. دالة التواصل مع جوجل
def ask_ahmed(text):
    is_first_reply = len(st.session_state.chat_history) == 0
    if is_first_reply:
        extra_instruction = "هذا أول رد لك، رحب بالمستخدم بلهجة عمانية واذكر بفخر أنك من برمجة أحمد بن بدر الصالحي (14 سنة)."
    else:
        extra_instruction = "خلك رزين وركز على الإجابة مباشرة ولا تكرر المدح إلا إذا سُئلت."

    system_instruction = (
        f"أنت ذكاء اصطناعي محترف. {extra_instruction} "
        "تحدث بلهجة عمانية قحة ورزينة إذا كانت المحادثة بالعربي. "
        "مبرمجك هو أحمد بن بدر الصالحي وفخره."
    )
    
    current_history = st.session_state.chat_history + [{"role": "user", "parts": [{"text": text}]}]
    payload = {
        "contents": current_history,
        "system_instruction": {"parts": [{"text": system_instruction}]}
    }
    
    try:
        response = requests.post(URL, json=payload, timeout=15)
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    except:
        return "السموحة يا بوبدر، الشبكة تعبانة شوي، حاول مرة ثانية!"

# 6. عرض الشات
for message in st.session_state.chat_history:
    role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(role):
        st.write(message["parts"][0]["text"])

# 7. خانة الكتابة والذكاء الهجين (نص + صور)
if prompt := st.chat_input("تحدث معي أو اطلب مني أرسم لك (مثال: ارسم سيارة)..."):
    with st.chat_message("user"):
        st.write(prompt)
    
    # فحص إذا كان المستخدم يريد صورة
    if "ارسم" in prompt or "صورة" in prompt or "image" in prompt.lower():
