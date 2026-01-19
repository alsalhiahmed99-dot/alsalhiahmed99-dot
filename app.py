import streamlit as st
import requests
import json
import random

# 1. إعدادات الصفحة
st.set_page_config(page_title="أحمد AI PRO", page_icon="🤖")

# 2. مفاتيح التشغيل
MY_KEY = st.secrets["GOOGLE_API_KEY"]
MODEL_NAME = "gemini-1.5-flash"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={MY_KEY}"

# 3. تصميم الواجهة
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

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 5. دالة التواصل (محدثة لإظهار الأخطاء الحقيقية)
def ask_ahmed(text):
    # تبسيط المحتوى جداً لتجنب رفض جوجل
    payload = {
        "contents": [{"role": "user", "parts": [{"text": text}]}]
    }
    try:
        response = requests.post(URL, json=payload, timeout=30)
        res_data = response.json()
        
        if response.status_code == 200:
            return res_data['candidates'][0]['content']['parts'][0]['text']
        else:
            # بيطلع لك رسالة الخطأ الحقيقية هنا
            error_msg = res_data.get('error', {}).get('message', 'خطأ مجهول')
            return f"خطأ فني من جوجل: {error_msg}"
    except Exception as e:
        return f"فشل الاتصال: {str(e)}"

# 6. عرض المحادثة
for message in st.session_state.chat_history:
    role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(role):
        st.write(message["parts"][0]["text"])

# 7. خانة الكتابة
if prompt := st.chat_input("اكتب شيئاً..."):
    with st.chat_message("user"):
        st.write(prompt)
    
    # فحص الصور (هذي الميزة تشتغل بسيرفر مختلف ومفروض ما تتعطل)
    if any(word in prompt.lower() for word in ["ارسم", "صورة", "image"]):
        with st.chat_message("assistant"):
            with st.spinner('أحمد AI يرسم...'):
                seed = random.randint(1, 99999)
                clean_p = prompt.replace("ارسم", "").replace("صورة", "").strip()
                img_url = f"https://pollinations.ai/p/{clean_p.replace(' ', '%20')}?width=1024&height=1024&seed={seed}&nologo=true"
                try:
                    img_res = requests.get(img_url, timeout=20)
                    st.image(img_res.content, caption=f"إبداع أحمد لـ: {clean_p}")
                    st.download_button("📥 حفظ الصورة", img_res.content, "ahmed_ai.png")
                except:
                    st.error("مشكلة في سيرفر الصور.")
    else:
        # رد نصي
        with st.spinner("أحمد AI يفكر..."):
            res = ask_ahmed(prompt)
            with st.chat_message("assistant"):
                st.write(res)
            st.session_state.chat_history.append({"role": "user", "parts": [{"text": prompt}]})
            st.session_
