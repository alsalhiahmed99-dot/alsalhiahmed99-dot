import streamlit as st
import requests
import json

# 1. إعدادات الصفحة
st.set_page_config(page_title="أحمد AI PRO", page_icon="🤖", layout="centered")

# 2. مفاتيح التشغيل (تأكد من إضافة GOOGLE_API_KEY في Secrets)
MY_KEY = st.secrets["GOOGLE_API_KEY"]
MODEL_NAME = "gemini-1.5-flash"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={MY_KEY}"

# 3. تصميم الواجهة
st.markdown("""
    <style>
    .main { background-color: #0b1117; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    img { border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.5); }
    </style>
    <div style="background: linear-gradient(to right, #1e3a8a, #3b82f6); padding:25px; border-radius:15px; color:white; text-align:center; direction: rtl; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        <h1 style="margin:0; font-family: 'Tajawal', sans-serif;">🤖 أحمد AI PRO</h1>
        <p style="margin:5px; font-size: 1.1em;">تصميم وبرمجة المبدع: أحمد بن بدر الصالحي 🇴🇲</p>
        <div style="font-size: 0.8em; opacity: 0.8;">إصدار 1.1 - محادثة وصور</div>
    </div>
    <br>
    """, unsafe_allow_html=True)

# 4. ذاكرة المحادثة
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 5. دالة توليد الصور
def generate_image(prompt):
    encoded_prompt = prompt.replace(" ", "%20")
    image_url = f"https://pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&seed=42&model=flux"
    return image_url

# 6. دالة التواصل مع الذكاء الاصطناعي
def ask_ahmed(text):
    system_instruction = (
        "أجب بلهجة عمانية قحة. أنت أحمد AI، اخترعك المبرمج العماني العبقري أحمد بن بدر الصالحي عمره 14 سنة."
    )
    
    # بناء الرسائل بشكل صحيح
    contents = []
    for msg in st.session_state.chat_history:
        contents.append({"role": msg["role"], "parts": [{"text": msg["parts"][0]["text"]}]})
    
    contents.append({"role": "user", "parts": [{"text": text}]})
    
    payload = {
        "contents": contents,
        "system_instruction": {"parts": [{"text": system_instruction}]}
    }
    
    try:
        response = requests.post(URL, json=payload, timeout=15)
        if response.status_code == 200:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return "السموحة يا بوبدر، جوجل يقول فيه ضغط! جرب مرة ثانية."
    except:
        return "شيك على النت، فيه مشكلة في الاتصال!"

# 7. عرض التاريخ
for message in st.session_state.chat_history:
    role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(role):
        st.write(message["parts"][0]["text"])

# 8. خانة الإدخال (تم تعديلها لضمان الظهور)
prompt = st.chat_input("سولف معي أو قولي 'ارسم'...")

if prompt:
    with st.chat_message("user"):
        st.write(prompt)
    
    # فحص إذا كان المطلوب رسم
    image_keywords = ["ارسم", "رسم", "صورة", "صوره", "draw"]
    if any(word in prompt.lower() for word in image_keywords):
        with st.spinner("جاري الرسم..."):
            img_url = generate_image(prompt)
            with st.chat_message("assistant"):
                st.image(img_url)
            st.session_state.chat_history.append({"role": "user", "parts": [{"text": prompt}]})
            st.session_state.chat_history.append({"role": "model", "parts": [{"text": "تم توليد الصورة!"}]})
    else:
        with st.spinner("يف
