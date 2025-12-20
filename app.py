import streamlit as st
import requests
import json

# 1. إعدادات المتصفح
st.set_page_config(page_title="أحمد AI PRO", page_icon="🤖")

# 2. مفاتيح التشغيل
MY_KEY = st.secrets["GOOGLE_API_KEY"]
TEXT_MODEL = "gemini-1.5-flash" # أو gemini-3-flash-preview إذا متاح لك
IMAGE_MODEL = "imagen-3.0-generate-001" # موديل الصور

TEXT_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{TEXT_MODEL}:generateContent?key={MY_KEY}"
# ملاحظة: توليد الصور أحياناً يتطلب API مختلف، لكن هذا التعديل يضيف "المنطق" لكودك
IMAGE_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{IMAGE_MODEL}:predict?key={MY_KEY}"

# 3. تصميم الواجهة (نفس تصميمك الرهيب)
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

# 5. دالة التواصل (محدثة لتشمل الصور)
def ask_ahmed(text):
    # إذا المستخدم طلب صورة
    if "صورة" in text or "صمم" in text or "image" in text.lower():
        return "IMAGE_REQUEST"

    system_instruction = (
        "أنت مساعد ذكي جداً. أجب بلهجة عمانية قحة وذكاء شديد. "
        "ممنوع أن تقول 'أنا أحمد AI' في بداية ردك أو وسطه. "
        "تذكر دائماً أن من اخترعك وصممك وبرمجك هو العبقري أحمد بن بدر الصالحي."
    )
    
    current_history = st.session_state.chat_history + [{"role": "user", "parts": [{"text": text}]}]
    payload = {
        "contents": current_history,
        "system_instruction": {"parts": [{"text": system_instruction}]}
    }
    
    try:
        response = requests.post(TEXT_URL, json=payload, timeout=15)
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    except:
        return "السموحة يا بوبدر، جوجل يقول فيه ضغط!"

# 6. عرض الشات
for message in st.session_state.chat_history:
    role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(role):
        st.write(message["parts"][0]["text"])

# 7. خانة الكتابة والتشغيل
if prompt := st.chat_input("تحدث مع أحمد AI..."):
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.spinner("جاري الاستجابة..."):
        res = ask_ahmed(prompt)
        
        if res == "IMAGE_REQUEST":
            # هنا تضع كود طلب الصورة من الـ API (إذا كان حسابك مفعلاً لـ Imagen)
            # بما أنك تستخدم streamlit، الأسهل حالياً استخدام ميزة توليد الصور الداخلية
            st.write("يا بوبدر، جاري تجهيز ميزة توليد الصور الفنية في ملف app.py المطور!")
            # ملاحظة: Imagen يحتاج إعدادات Predict خاصة في Google Cloud
        else:
            with st.chat_message("assistant"):
                st.write(res)
            st.session_state.chat_history.append({"role": "user", "parts": [{"text": prompt}]})
            st.session_state.chat_history.append({"role": "model", "parts": [{"text": res}]})
