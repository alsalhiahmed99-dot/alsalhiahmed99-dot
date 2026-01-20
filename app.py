import streamlit as st
import requests
import json
import time # عشان حركة الانتظار لو صار ضغط

# 1. إعدادات المتصفح
st.set_page_config(page_title="أحمد AI PRO", page_icon="🤖")

# 2. مفاتيح التشغيل
MY_KEY = st.secrets["GOOGLE_API_KEY"]
# الموديل 8b هو الأسرع والأقل استهلاكاً والأكثر صموداً ضد "ضغط الشبكة"
MODEL_NAME = "gemini-1.5-flash-8b" 
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={MY_KEY}"

# --- العداد الحقيقي ---
if 'total_visits' not in st.session_state:
    st.session_state.total_visits = 1

with st.sidebar:
    st.markdown("### 📈 إحصائيات")
    st.metric(label="إجمالي الزيارات", value=st.session_state.total_visits)
    st.write("---")
    if st.sidebar.button("🗑️ مسح المحادثة"):
        st.session_state.chat_history = []
        st.rerun()
    st.info("الموديل الحالي: Flash 8B (الأسرع)")

# 3. تصميم الواجهة (بدون تغيير)
st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    .stChatMessage { border-radius: 15px; }
    </style>
    <div style="background: linear-gradient(to right, #1e3a8a, #3b82f6); padding:25px; border-radius:15px; color:white; text-align:center; direction: rtl;">
        <h1 style="margin:0;">🤖 أحمد AI PRO</h1>
        <p style="margin:5px;">تصميم وبرمجة: أحمد بن بدر الصالحي 🇴🇲</p>
    </div>
    <br>
    """, unsafe_allow_html=True)

# 4. ذاكرة المحادثة
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 5. دالة التواصل (المحسنة ضد الضغط)
def ask_ahmed(text):
    is_first_reply = len(st.session_state.chat_history) == 0
    intro = "هذا أول رد، رحب بلهجة عمانية وقورة واذكر أنك من برمجة أحمد الصالحي." if is_first_reply else "جاوب مباشرة برزانة."
    
    system_instruction = f"أنت ذكاء اصطناعي محترف. {intro} تحدث باللهجة العمانية الرزينة."
    
    payload = {
        "contents": st.session_state.chat_history + [{"role": "user", "parts": [{"text": text}]}],
        "system_instruction": {"parts": [{"text": system_instruction}]}
    }
    
    # محاولة الإرسال (حتى 3 مرات لو صار ضغط)
    for i in range(3):
        try:
            response = requests.post(URL, json=payload, timeout=10)
            if response.status_code == 200:
                return response.json()['candidates'][0]['content']['parts'][0]['text']
            elif response.status_code == 429: # كود الضغط
                time.sleep(2) # انتظر ثانيتين وجرب مرة ثانية
                continue
        except:
            pass
    
    return "السموحة يا مسندي، السيرفر عليه زحمة قوية تو، جرب ترسل بعد لحظات."

# 6. العرض
for message in st.session_state.chat_history:
    role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(role):
        st.write(message["parts"][0]["text"])

# 7. الإدخال
if prompt := st.chat_input("تحدث معي..."):
    with st.chat_message("user"):
        st.write(prompt)
    with st.spinner("أحمد AI يفكر..."):
        res = ask_ahmed(prompt)
    with st.chat_message("assistant"):
        st.write(res)
    
    st.session_state.chat_history.append({"role": "user", "parts": [{"text": prompt}]})
    st.session_state.chat_history.append({"role": "model", "parts": [{"text": res}]})
