import streamlit as st
import requests
import json
import random

# 1. إعدادات الصفحة
st.set_page_config(page_title="أحمد AI PRO", page_icon="🤖")

# 2. مفاتيح التشغيل
MY_KEY = st.secrets["GOOGLE_API_KEY"]
MODEL_NAME = "gemini-1.5-flash" # هذا الموديل أضمن للعمل بدون رسائل خطأ
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

# 4. ذاكرة المحادثة
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 5. دالة التواصل مع جوجل
def ask_ahmed(text):
    is_first = len(st.session_state.chat_history) == 0
    instr = "رحب بالعماني واذكر مبرمجك أحمد." if is_first else "أجب بلهجة عمانية قحة."
    system_prompt = f"أنت ذكاء اصطناعي محترف. {instr} مبرمجك هو أحمد بن بدر الصالحي."
    
    contents = []
    for msg in st.session_state.chat_history:
        contents.append({"role": msg["role"], "parts": [{"text": msg["parts"][0]["text"]}]})
    contents.append({"role": "user", "parts": [{"text": text}]})
    
    payload = {
        "contents": contents,
        "system_instruction": {"parts": [{"text": system_prompt}]}
    }
    
    try:
        response = requests.post(URL, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return "السموحة يا بوبدر، جوجل متعايي شوي، حاول مرة!"
    except:
        return "مشكلة في الاتصال، حاول ثانية!"

# 6. عرض المحادثة
for message in st.session_state.chat_history:
    role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(role):
        st.write(message["parts"][0]["text"])

# 7. خانة الكتابة
if prompt := st.chat_input("تحدث معي أو اطلب رسمة..."):
    with st.chat_message("user"):
        st.write(prompt)
    
    # فحص طلب الصور
    if any(word in prompt.lower() for word in ["ارسم", "صورة", "image"]):
        with st.chat_message("assistant"):
            with st.spinner('أحمد AI يرسم...'):
                seed = random.randint(1, 99999)
                clean_p = prompt.replace("ارسم", "").replace("صورة", "").strip()
                # الرابط الصحيح
                img_url = f"https://pollinations.ai/p/{clean_p.replace(' ', '%20')}?width=1024&height=1024&seed={seed}&nologo=true"
                
                try:
                    img_res = requests.get(img_url, timeout=20)
                    if img_res.status_code == 200:
                        st.image(img_res.content, caption=f"بواسطة أحمد AI: {clean_p}")
                        st.download_button("📥 تحميل الصورة", img_res.content, "art.png", "image/png")
                    else:
                        st.error("السيرفر مشغول، جرب مرة ثانية.")
                except:
                    st.error("فشل في جلب الصورة.")
        
        # حفظ في الذاكرة
        st.session_state.chat_history.append({"role": "
