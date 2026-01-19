import streamlit as st
import requests
import json
import random

# 1. إعدادات المتصفح
st.set_page_config(page_title="أحمد AI PRO", page_icon="🤖")

# 2. مفاتيح التشغيل
MY_KEY = st.secrets["GOOGLE_API_KEY"]
MODEL_NAME = "gemini-3-flash-preview"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={MY_KEY}"

# 3. تصميم الواجهة
st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    .stChatMessage { border-radius: 15px; }
    </style>
    <div style="background: linear-gradient(to right, #1e3a8a, #3b82f6); padding:25px; border-radius:15px; color:white; text-align:center; direction: rtl; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        <h1 style="margin:0; font-family: 'Tajawal', sans-serif;">🤖 أحمد AI PRO</h1>
        <p style="margin:5px; font-size: 1.1em;">تصميم وبرمجة: أحمد بن بدر الصالحي 🇴🇲</p>
        <div style="font-size: 0.8em; opacity: 0.8;">إصدار الذكاء الاصطناعي 1.0 (دعم الصور)</div>
    </div>
    <br>
    """, unsafe_allow_html=True)

# 4. ذاكرة المحادثة
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 5. دالة التواصل مع جوجل
def ask_ahmed(text):
    is_first_reply = len(st.session_state.chat_history) == 0
    extra_instruction = "رحب بالمستخدم بلهجة عمانية واذكر فخرك بمبرمجك أحمد." if is_first_reply else "أجب مباشرة بلهجة عمانية رزينة."
    
    system_instruction = (
        f"أنت ذكاء اصطناعي محترف. {extra_instruction} "
        "تحدث بلهجة عمانية قحة ورزينة. مبرمجك هو أحمد بن بدر الصالحي."
    )
    
    current_history = st.session_state.chat_history + [{"role": "user", "parts": [{"text": text}]}]
    payload = {
        "contents": current_history,
        "system_instruction": {"parts": [{"text": system_instruction}]}
    }
    
    try:
        response = requests.post(URL, json=payload, timeout=15)
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "السموحة يا بوبدر، جوجل متعايي شوي، حاول مرة!"

# 6. عرض الشات القديم
for message in st.session_state.chat_history:
    role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(role):
        st.write(message["parts"][0]["text"])

# 7. خانة الكتابة (الذكاء المدمج)
if prompt := st.chat_input("تحدث معي أو اطلب رسمة..."):
    with st.chat_message("user"):
        st.write(prompt)
    
    # تحويل النص لـ lowercase للفحص
    p_low = prompt.lower()
    if any(word in p_low for word in ["ارسم", "صورة", "image", "draw"]):
        with st.chat_message("assistant"):
            with st.spinner('أحمد AI جالس يرسم لك...'):
                seed = random.randint(1, 99999)
                # تنظيف الكلمات المفتاحية للحصول على الوصف فقط
                clean_p = prompt.replace("ارسم", "").replace("صورة", "").replace("image", "").replace("Image", "").strip()
                # السطر اللي كان فيه الخطأ (تم إصلاحه بإضافة علامة التنصيص في النهاية)
                image_url = f"https://pollinations.ai/p/{clean_p.replace(' ', '%20')}?width=1024&height=1024&seed={seed}&nologo=true"
                
                try:
                    # تحميل الصورة وعرضها كبيانات لضمان عدم الخروج من التطبيق
                    img_res = requests.get(image_url, timeout=20)
                    if img_res.status_code == 200:
                        st.image(img_res.content, caption=f"إبداع أحمد AI لـ: {clean_p}", use_container_width=True)
                        st.download_button(label="📥 تحميل الصورة", data=img_res.content, file_name="ahmed_ai_art.png", mime="image/png")
                    else:
                        st.error("الموقع مشغول شوي، جرب بعد ثواني.")
                except:
                    st.error("أفا! الرسام تعبان اليوم، حاول مرة ثانية.")
                
                st.session_state.chat_history.append({"role": "user", "parts": [{"text": prompt}]})
                st.session_state.chat_history.append({"role": "model", "parts": [{"text": f"تم رسم: {clean_p}"}]})
    
    else:
        with st.spinner("أحمد AI يفكر..."):
            res = ask_ahmed(prompt)
        with st.chat_message("assistant"):
            st.write(res)
        st.session_state.chat_history.append({"role": "user", "parts": [{"text": prompt}]})
        st.session_state.chat_history.append({"role": "model", "parts": [{"text": res}]})
