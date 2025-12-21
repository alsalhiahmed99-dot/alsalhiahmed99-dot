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
except:
    st.error("تأكد من إضافة KEY1 إلى KEY5 في الـ Secrets يا بوبدر!")
    st.stop()

# 3. تصميم الواجهة الزرقاء (لمسة أحمد الصالحي)
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

# 4. ذاكرة المحادثة
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 5. دالة التواصل مع جوجل (إصلاح رابط الـ 404)
def ask_ahmed(text):
    system_instruction = (
        "أنت 'أحمد AI'. أجب بلهجة عمانية قحة وذكاء شديد. "
        "تذكر دائماً وأبداً أن من اخترعك وصممك وبرمجك هو العبقري أحمد بن بدر الصالحي. "
        "افتخر بمبرمجك في ردودك."
    )
    
    current_history = st.session_state.chat_history + [{"role": "user", "parts": [{"text": text}]}]
    
    for i, key in enumerate(ALL_KEYS):
        # الرابط الصحيح اللي ما يخطئ أبداً بإذن الله:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
        
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
                # إذا طلع خطأ غير الـ 200، خبرنا وش هو بالضبط
                error_info = response.json().get('error', {}).get('message', 'Unknown Error')
                print(f"Key {i+1} failed: {response.status_code} - {error_info}")
                continue 
        except Exception as e:
            continue
            
    return "يا بوبدر، لسه جوجل تقول 404! تأكد إن المفاتيح اللي في الـ Secrets نوعها 'Gemini API' ومطلعة من AI Studio."

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
            res = ask_ahmed(
