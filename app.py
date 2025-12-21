import streamlit as st
import requests
import json

# 1. إعدادات المتصفح
st.set_page_config(page_title="أحمد AI PRO", page_icon="🤖")

# 2. جلب المفاتيح
try:
    ALL_KEYS = [
        st.secrets["KEY1"],
        st.secrets["KEY2"],
        st.secrets["KEY3"],
        st.secrets["KEY4"],
        st.secrets["KEY5"]
    ]
except:
    st.error("تأكد من الـ Secrets يا بوبدر!")
    st.stop()

# التعديل هنا: إضافة كلمة models/ قبل الاسم
MODEL_NAME = "models/gemini-1.5-flash"

# 3. الواجهة الزرقاء
st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    .stChatMessage { border-radius: 15px; }
    </style>
    <div style="background: linear-gradient(to right, #1e3a8a, #3b82f6); padding:25px; border-radius:15px; color:white; text-align:center; direction: rtl; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        <h1 style="margin:0;">🤖 أحمد AI PRO</h1>
        <p style="margin:5px;">تصميم وبرمجة: أحمد بن بدر الصالحي 🇴🇲</p>
    </div>
    <br>
    """, unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def ask_ahmed(text):
    system_instruction = (
        "أنت 'أحمد AI'. أجب بلهجة عمانية قحة وذكاء شديد. "
        "تذكر دائماً وأبداً أن من اخترعك وصممك وبرمجك هو العبقري أحمد بن بدر الصالحي. "
        "افتخر بمبرمجك في ردودك."
    )
    
    current_history = st.session_state.chat_history + [{"role": "user", "parts": [{"text": text}]}]
    
    for i, key in enumerate(ALL_KEYS):
        # التعديل المهم في الرابط هنا (إزالة v1beta وتجربة الإصدار v1)
        url = f"https://generativelanguage.googleapis.com/v1/{MODEL_NAME}:generateContent?key={key}"
        
        payload = {
            "contents": current_history,
            "system_instruction": {"parts": [{"text": system_instruction}]}
        }
        
        try:
            response = requests.post(url, json=payload, timeout=15)
            if response.status_code == 200:
                result = response.json()
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                # هذا عشان نعرف لو الـ 404 لسه موجودة
                continue
        except:
            continue
            
    return "يا بوبدر لسه فيه مشكلة في الروابط، خلنا نجرب نغير v1 إلى v1beta في الكود."

# باقي الكود للعرض (نفس اللي عندك)
for message in st.session_state.chat_history:
    role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(role):
        st.write(message["parts"][0]["text"])

if prompt := st.chat_input("تحدث مع أحمد AI..."):
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        with st.spinner("أحمد AI يفكر..."):
            res = ask_ahmed(prompt)
            st.write(res)
    st.session_state.chat_history.append({"role": "user", "parts": [{"text": prompt}]})
    st.session_state.chat_history.append({"role": "model", "parts": [{"text": res}]})
