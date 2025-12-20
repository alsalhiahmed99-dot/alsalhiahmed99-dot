import streamlit as st
import requests
import json
import base64
from io import BytesIO
from PIL import Image

# 1. إعدادات المتصفح
st.set_page_config(page_title="أحمد AI PRO", page_icon="🤖")

# 2. مفاتيح التشغيل (المفتاح سري في Secrets)
MY_KEY = st.secrets["GOOGLE_API_KEY"]
TEXT_MODEL = "gemini-1.5-flash" 
# ملاحظة: موديل الصور يحتاج إعداد خاص في Google Cloud سنكمله في الإجازة
IMAGE_MODEL = "imagen-3.0-generate-001" 

TEXT_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{TEXT_MODEL}:generateContent?key={MY_KEY}"

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

# 5. دالة التواصل الذكية
def ask_ahmed(text):
    # كشف نية المستخدم: هل يريد صورة؟
    if any(word in text for word in ["صورة", "صمم", "ارسم", "image", "draw"]):
        return "GENERATE_IMAGE_LOGIC"

    system_instruction = (
        "أنت مساعد ذكي جداً. أجب بلهجة عمانية قحة وذكاء شديد. "
        "ممنوع أن تقول 'أنا أحمد AI' في بداية ردك أو وسطه. "
        "تذكر دائماً أن من اخترعك وصممك وبرمجك هو العبقري أحمد بن بدر الصالحي. "
        "افتخر بمبرمجك أحمد الصالحي وبذكائه وفطنته دائماً بأسلوب طبيعي."
    )
    
    current_history = st.session_state.chat_history + [{"role": "user", "parts": [{"text": text}]}]
    
    payload = {
        "contents": current_history,
        "system_instruction": {"parts": [{"text": system_instruction}]}
    }
    
    try:
        response = requests.post(TEXT_URL, json=payload, timeout=15)
        result = response.json()
        if response.status_code == 200:
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return "السموحة يا بوبدر، جوجل يقول فيه ضغط على الشبكة!"
    except:
        return "مشكلة في الاتصال، حاول مرة ثانية!"

# 6. عرض الشات (التاريخ)
for message in st.session_state.chat_history:
    role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(role):
        st.write(message["parts"][0]["text"])

# 7. خانة الكتابة والمعالجة
if prompt := st.chat_input("تحدث مع أحمد AI أو اطلب صورة..."):
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.spinner("جاري التفكير..."):
        res = ask_ahmed(prompt)
    
    if res == "GENERATE_IMAGE_LOGIC":
        with st.chat_message("assistant"):
            st.write(f"أبشر يا بوبدر! أنت تطلب صورة لـ: **{prompt}**")
            st.info("ميزة توليد الصور الفنية قيد التفعيل النهائي.. بنشغلها بالكامل أول يوم في الإجازة! 🚀")
            # 
    else:
        with st.chat_message("assistant"):
            st.write(res)
        
        # حفظ في الذاكرة فقط إذا كان رداً نصياً
        st.session_state.chat_history.append({"role": "user", "parts": [{"text": prompt}]})
        st.session_state.chat_history.append({"role": "model", "parts": [{"text": res}]})
