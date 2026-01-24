import streamlit as st
import requests
import json
import random

# 1. إعدادات المتصفح
st.set_page_config(page_title="أحمد AI PRO", page_icon="🤖")

# 2. إعدادات المفاتيح المتعددة
# تأكد إنك حاط KEYS في السيكريت كقائمة ["key1", "key2"]
ALL_KEYS = st.secrets["KEYS"]
MODEL_NAME = "gemini-3-flash-preview"

# --- الشريط الجانبي (معلومات حقيقية) ---
with st.sidebar:
    st.markdown("### 🛠️ معلومات النظام")
    st.info(f"عدد المفاتيح النشطة: {len(ALL_KEYS)}")
    st.write("---")
    st.markdown("### 👨‍💻 المبرمج")
    st.write("أحمد بن بدر الصالحي")
    st.caption("عماني، 14 سنة 🇴🇲")
    st.write("---")
    st.success("الحالة: يعمل بكفاءة عالية")

# 3. تصميم الواجهة الأصلي (مثل ما هو بالضبط)
st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    .stChatMessage { border-radius: 15px; }
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

# 5. دالة التواصل مع جوجل (معدلة للتبديل بين المفاتيح)
def ask_ahmed(text):
    # اختيار مفتاح عشوائي من القائمة لضمان عدم توقف البرنامج
    CURRENT_KEY = random.choice(ALL_KEYS)
    URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={CURRENT_KEY}"

    is_first_reply = len(st.session_state.chat_history) == 0
    if is_first_reply:
        extra_instruction = "هذا أول رد لك في المحادثة، رحب بالمستخدم بلهجة عمانية واذكر بفخر أنك من برمجة العبقري أحمد بن بدر الصالحي (14 سنة)."
    else:
        extra_instruction = "هذا ليس الرد الأول، خلك رزين وركز على إجابة السؤال مباشرة."

    system_instruction = (
        f"أنت ذكاء اصطناعي محترف. {extra_instruction} "
        "تحدث باللهجة العمانية القحة والرزينة."
    )
    
    current_history = st.session_state.chat_history + [{"role": "user", "parts": [{"text": text}]}]
    payload = {
        "contents": current_history,
        "system_instruction": {"parts": [{"text": system_instruction}]}
    }
    
    try:
        response = requests.post(URL, json=payload, timeout=15)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        return "السموحة، فيه ضغط على الشبكة! جرب ترسل مرة ثانية."
    except:
        return "مشكلة في الاتصال بالخادم السحابي!"

# 6. عرض الشات
for message in st.session_state.chat_history:
    role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(role):
        st.write(message["parts"][0]["text"])

# 7. خانة الكتابة
if prompt := st.chat_input("تحدث معي..."):
    with st.chat_message("user"):
        st.write(prompt)
    with st.spinner("أحمد AI يفكر بذكاء..."):
        res = ask_ahmed(prompt)
    with st.chat_message("assistant"):
        st.write(res)
    
    st.session_state.chat_history.append({"role": "user", "parts": [{"text": prompt}]})
    st.session_state.chat_history.append({"role": "model", "parts": [{"text": res}]})
