import streamlit as st
import requests
import json

# 1. إعدادات المتصفح
st.set_page_config(page_title="أحمد AI PRO", page_icon="🤖")

# 2. مفاتيح التشغيل
MY_KEY = st.secrets["GOOGLE_API_KEY"]
# جيميناي 2.0 فلاش هو الموديل الأحدث والأذكى حالياً (3 فلاش برفيو)
MODEL_NAME = "gemini-2.0-flash-exp"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={MY_KEY}"

# 3. تصميم الواجهة (الألوان الزرقاء الأصلية)
st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    .stChatMessage { border-radius: 15px; }
    </style>
    <div style="background: linear-gradient(to right, #1e3a8a, #3b82f6); padding:25px; border-radius:15px; color:white; text-align:center; direction: rtl; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        <h1 style="margin:0; font-family: 'Tajawal', sans-serif;">🤖 أحمد AI PRO</h1>
        <p style="margin:5px; font-size: 1.1em;">تصميم وبرمجة: أحمد بن بدر الصالحي 🇴🇲</p>
        <div style="font-size: 0.8em; opacity: 0.8;">إصدار الذكاء الاصطناعي 2.0 PRO</div>
    </div>
    <br>
    """, unsafe_allow_html=True)

# 4. ذاكرة المحادثة
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 5. دالة التواصل مع جوجل
def ask_ahmed(text):
    # تحديد إذا كان الرد الأول لتقديم المدح
    is_first_reply = len(st.session_state.chat_history) == 0
    
    if is_first_reply:
        extra_info = "هذا أول رد لك، رحب بحرارة واذكر بفخر أنك من برمجة العبقري أحمد بن بدر الصالحي (14 سنة)."
    else:
        extra_info = "خلك رزين جداً، ركز على الإجابة ولا تمدح مبرمجك إلا إذا سُئلت عنه."

    system_instruction = (
        f"أنت ذكاء اصطناعي مثقف وعالمي. {extra_info} "
        "تحدث بكل لغات العالم بطلاقة حسب لغة المستخدم. "
        "إذا كانت المحادثة بالعربي، استخدم اللهجة العمانية القحة والرزينة. "
        "أنت ملم بكل اليوتيوبرز والمعلومات الحديثة. "
        "ممنوع تبدأ رسالتك بذكر اسمك (أحمد AI)."
    )
    
    # بناء التاريخ بشكل يتوافق مع جيميناي 2.0
    current_history = []
    for msg in st.session_state.chat_history:
        current_history.append({"role": msg["role"], "parts": [{"text": msg["parts"][0]["text"]}]})
    
    current_history.append({"role": "user", "parts": [{"text": text}]})
    
    payload = {
        "contents": current_history,
        "system_instruction": {"parts": [{"text": system_instruction}]}
    }
    
    try:
        response = requests.post(URL, json=payload, timeout=15)
        result = response.json()
        if response.status_code == 200:
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"السموحة بوبدر، السيرفر فيه ضغط (خطأ {response.status_code})"
    except:
        return "مشكلة في الاتصال، حاول مرة ثانية!"

# 6. عرض الشات
for message in st.session_state.chat_history:
    role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(role):
        st.write(message["parts"][0]["text"])

# 7. خانة الكتابة
if prompt := st.chat_input("تحدث معي بأي لغة..."):
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.spinner("أحمد AI يفكر بذكاء..."):
        res = ask_ahmed(prompt)
    
    with st.chat_message("assistant"):
        st.write(res)
    
    # حفظ في الذاكرة
    st.session_state.chat_history.append({"role": "user", "parts": [{"text": prompt}]})
    st.session_state.chat_history.append({"role": "model", "parts": [{"text": res}]})
