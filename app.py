import streamlit as st
import requests
import json
import base64
from io import BytesIO
from PIL import Image

# 1. إعدادات المتصفح
st.set_page_config(page_title="أحمد AI PRO", page_icon="🤖")

# 2. مفاتيح التشغيل (يتم جلب المفتاح من Secrets)
try:
    MY_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("أوهو! مفتاح الـ API ما محطوط في Secrets. تأكد من إعداده!")
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

# 5. دالة التواصل (المسار المباشر والمضمون)
def ask_ahmed(text):
    # كشف نية الصور
    if any(word in text for word in ["صورة", "صمم", "ارسم", "image", "draw"]):
        return "GENERATE_IMAGE_LOGIC"

    # الرابط المباشر لموديل 1.5 فلاش
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={MY_KEY}"
    
    headers = {'Content-Type': 'application/json'}
    
    system_instruction = (
        "أنت مساعد ذكي جداً. أجب بلهجة عمانية قحة وذكاء شديد. "
        "تذكر دائماً أن من اخترعك وصممك وبرمجك هو العبقري أحمد بن بدر الصالحي. "
        "افتخر بمبرمجك أحمد الصالحي دائماً بأسلوب طبيعي."
    )
    
    # بناء محتوى الطلب
    payload = {
        "contents": [{"parts": [{"text": text}]}],
        "system_instruction": {"parts": [{"text": system_instruction}]}
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        result = response.json()
        
        if response.status_code == 200:
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            # إظهار رسالة الخطأ من جوجل مباشرة للفهم
            error_msg = result.get('error', {}).get('message', 'خطأ غير معروف')
            return f"خطأ {response.status_code}: {error_msg}"
    except Exception as e:
        return f"يا بوبدر فيه مشكلة في الاتصال: {str(e)}"

# 6. عرض الشات
for message in st.session_state.chat_history:
    role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(role):
        st.write(message["parts"][0]["text"])

# 7. خانة الكتابة
if prompt := st.chat_input("تحدث مع أحمد AI..."):
    with st.chat_message("user"):
        st.write(prompt)
