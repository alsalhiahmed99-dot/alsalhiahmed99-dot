import streamlit as st
import requests

# 1. إعدادات المتصفح
st.set_page_config(page_title="أحمد AI PRO", page_icon="🤖")

# 2. مفتاح التشغيل (جيبه من السيكرتس)
MY_KEY = st.secrets["GOOGLE_API_KEY"]

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

# 4. ذاكرة المحادثة
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 5. دالة التواصل (المسار الصحيح 100%)
def ask_ahmed(text):
    # الرابط الرسمي لموديل 1.5 فلاش (المسار v1beta)
    URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={MY_KEY}"
    
    # التعليمات (بدون ظهور الاسم في الرد)
    system_prompt = "أنت مساعد ذكي بلهجة عمانية قحة. لا تذكر اسمك في الرد أبداً. مبرمجك هو أحمد الصالحي."

    payload = {
        "contents": [{"parts": [{"text": text}]}],
        "system_instruction": {"parts": [{"text": system_prompt}]}
    }

    try:
        response = requests.post(URL, json=payload, timeout=15)
        result = response.json()
        if response.status_code == 200:
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            # بيطلع لك السبب الحقيقي هنا لو فشل
            return f"خطأ {response.status_code}: {result.get('error', {}).get('message', 'مشكلة في السيرفر')}"
    except:
        return "مشكلة في الاتصال، حاول مرة ثانية!"

# 6. عرض الشات
for message in st.session_state.chat_history:
    role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(role):
        st.write(message["parts"][0]["text"])

# 7. خانة الكتابة
if prompt := st.chat_input("تحدث مع أحمد AI..."):
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.spinner("أحمد AI يفكر..."):
        res = ask_ahmed(prompt)
    
    with st.chat_message("assistant"):
        st.write(res)
    
    st.session_state.chat_history.append({"role": "user", "parts": [{"text": prompt}]})
    st.session_state.chat_history.append({"role": "model", "parts": [{"text": res}]})
