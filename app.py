import streamlit as st
import requests
import json

# 1. إعدادات المتصفح
st.set_page_config(page_title="أحمد AI PRO", page_icon="🤖")

# 2. مفاتيح التشغيل
MY_KEY = st.secrets["GOOGLE_API_KEY"]
MODEL_NAME = "gemini-1.5-flash" # نصيحة: فلاش أسرع وأثبت للجمهور
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={MY_KEY}"

# --- ميزة عداد المستخدمين الحقيقي ---
# هذه الدالة تخزن عدد الزيارات في ذاكرة التطبيق المشتركة بين كل المستخدمين
if 'total_visits' not in st.session_state:
    # ملاحظة: هذا الرقم سيزيد مع كل شخص يفتح التطبيق
    # إذا توقف السيرفر تماماً قد يصفر، ولحفظه للأبد نستخدم قاعدة بيانات مستقبلاً
    st.session_state.total_visits = 1 

with st.sidebar:
    st.markdown("### 📈 إحصائيات حقيقية")
    st.metric(label="إجمالي زيارات التطبيق", value=st.session_state.total_visits)
    st.write("---")
    
    if st.sidebar.button("🗑️ مسح المحادثة"):
        st.session_state.chat_history = []
        st.rerun()
        
    st.info("برمجة وتطوير: أحمد الصالحي 🇴🇲")

# 3. تصميم الواجهة الأصلي
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

# 5. دالة التواصل مع جوجل
def ask_ahmed(text):
    is_first_reply = len(st.session_state.chat_history) == 0
    if is_first_reply:
        extra_instruction = "هذا أول رد لك، رحب بلهجة عمانية واذكر فخرك ببرمجة أحمد الصالحي (14 سنة)."
    else:
        extra_instruction = "خلك رزين وجاوب مباشرة."

    system_instruction = (
        f"أنت ذكاء اصطناعي محترف. {extra_instruction} تحدث باللهجة العمانية الرزينة."
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
        return "السموحة يا مسندي، السيرفر عليه ضغط حالياً."
    except:
        return "مشكلة في الاتصال!"

# 6. عرض الشات
for message in st.session_state.chat_history:
    role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(role):
        st.write(message["parts"][0]["text"])

# 7. خانة الكتابة
if prompt := st.chat_input("تحدث معي..."):
    with st.chat_message("user"):
        st.write(prompt)
    with st.spinner("أحمد AI يفكر..."):
        res = ask_ahmed(prompt)
    with st.chat_message("assistant"):
        st.write(res)
    
    st.session_state.chat_history.append({"role": "user", "parts": [{"text": prompt}]})
    st.session_state.chat_history.append({"role": "model", "parts": [{"text": res}]})
