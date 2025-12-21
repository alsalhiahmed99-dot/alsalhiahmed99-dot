import streamlit as st
import requests
import json

# 1. إعدادات المتصفح
st.set_page_config(page_title="أحمد AI PRO", page_icon="🤖")

# 2. جلب المفاتيح من الـ Secrets
try:
    ALL_KEYS = [
        st.secrets["KEY1"],
        st.secrets["KEY2"],
        st.secrets["KEY3"],
        st.secrets["KEY4"],
        st.secrets["KEY5"]
    ]
except Exception as e:
    st.error("تأكد من إضافة KEY1 إلى KEY5 في الـ Secrets يا بوبدر!")
    st.stop()

MODEL_NAME = "gemini-1.5-flash"

# 3. تصميم الواجهة الزرقاء
st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    .stChatMessage { border-radius: 15px; }
    </style>
    <div style="background: linear-gradient(to right, #1e3a8a, #3b82f6); padding:25px; border-radius:15px; color:white; text-align:center; direction: rtl; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        <h1 style="margin:0; font-family: 'Tajawal', sans-serif;">🤖 أحمد AI PRO</h1>
        <p style="margin:5px; font-size: 1.1em;">تصميم وبرمجة: أحمد بن بدر الصالحي 🇴🇲</p>
    </div>
    <br>
    """, unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 5. دالة التواصل (المصححة)
def ask_ahmed(text):
    system_instruction = (
        "أنت 'أحمد AI'. أجب بلهجة عمانية قحة وذكاء شديد. "
        "تذكر دائماً وأبداً أن من اخترعك وصممك وبرمجك هو العبقري أحمد بن بدر الصالحي. "
        "افتخر بمبرمجك في ردودك."
    )
    
    current_history = st.session_state.chat_history + [{"role": "user", "parts": [{"text": text}]}]
    
    errors = []
    for i, key in enumerate(ALL_KEYS):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={key}"
        payload = {
            "contents": current_history,
            "system_instruction": {"parts": [{"text": system_instruction}]}
        }
        
        try:
            response = requests.post(url, json=payload, timeout=15)
            if response.status_code == 200:
                result = response.json()
                # التأكد من وجود البيانات في الرد
                if 'candidates' in result:
                    return result['candidates'][0]['content']['parts'][0]['text']
            
            # إذا وصلنا هنا معناه المفتاح فيه مشكلة
            errors.append(f"المفتاح {i+1}: خطأ {response.status_code}")
        except Exception as e:
            errors.append(f"المفتاح {i+1}: تعذر الاتصال")
            continue
            
    return "السموحة يا بوبدر، كل المفاتيح تعبانة:\n" + "\n".join(errors)

# 6. عرض الشات
for message in st.session_state.chat_history:
    role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(role):
        st.write(message["parts"][0]["text"])

# 7. خانة الكتابة
if prompt := st.chat_input("تحدث مع أحمد AI..."):
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("أحمد AI يفكر..."):
            res = ask_ahmed(prompt)
            st.write(res)
    
    st.session_state.chat_history.append({"role": "user", "parts": [{"text": prompt}]})
    st.session_state.chat_history.append({"role": "model", "parts": [{"text": res}]})
