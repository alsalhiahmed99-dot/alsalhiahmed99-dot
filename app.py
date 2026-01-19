import streamlit as st
import requests
import json
import random

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="أحمد AI PRO", page_icon="🤖")

# 2. مفاتيح التشغيل (تأكد من وجود GOOGLE_API_KEY في Secrets)
MY_KEY = st.secrets["GOOGLE_API_KEY"]
MODEL_NAME = "gemini-1.5-flash"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={MY_KEY}"

# 3. تصميم الواجهة (ستايل احترافي وعماني)
st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    </style>
    <div style="background: linear-gradient(to right, #1e3a8a, #3b82f6); padding:25px; border-radius:15px; color:white; text-align:center; direction: rtl;">
        <h1 style="margin:0; font-family: 'Tajawal', sans-serif;">🤖 أحمد AI PRO</h1>
        <p style="margin:5px; font-size: 1.1em;">تصميم وبرمجة: أحمد بن بدر الصالحي 🇴🇲</p>
    </div>
    <br>
    """, unsafe_allow_html=True)

# 4. إدارة ذاكرة المحادثة
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 5. دالة التواصل مع ذكاء جوجل الاصطناعي
def ask_ahmed(text):
    is_first = len(st.session_state.chat_history) == 0
    instr = "رحب بالعماني واذكر مبرمجك أحمد الصالحي." if is_first else "أجب بلهجة عمانية قحة ورزينة."
    system_prompt = f"أنت ذكاء اصطناعي محترف. {instr} مبرمجك هو أحمد بن بدر الصالحي عمره 14 سنة."
    
    payload = {
        "contents": [{"role": "user", "parts": [{"text": text}]}],
        "system_instruction": {"parts": [{"text": system_prompt}]}
    }
    try:
        response = requests.post(URL, json=payload, timeout=30)
        res_data = response.json()
        if response.status_code == 200:
            return res_data['candidates'][0]['content']['parts'][0]['text']
        else:
            error_msg = res_data.get('error', {}).get('message', 'خطأ غير معروف')
            return f"السموحة يا بوبدر، جوجل يقول: {error_msg}"
    except Exception as e:
        return f"فشل في الاتصال: {str(e)}"

# 6. عرض الرسائل السابقة من الذاكرة
for message in st.session_state.chat_history:
    role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(role):
        st.write(message["parts"][0]["text"])

# 7. منطقة الإدخال (النص والصور)
if prompt := st.chat_input("تحدث معي أو اطلب رسمة..."):
    with st.chat_message("user"):
        st.write(prompt)
    
    # فحص إذا كان الطلب يتضمن رسم صورة
    p_low = prompt.lower()
    if any(word in p_low for word in ["ارسم", "صورة", "image", "draw"]):
        with st.chat_message("assistant"):
            with st.spinner('أحمد AI جاري الإبداع في الرسم...'):
                seed = random.randint(1, 99999)
                clean_p = prompt.replace("ارسم", "").replace("صورة", "").replace("image", "").strip()
                img_url = f"https://pollinations.ai/p/{clean_p.replace(' ', '%20')}?width=1024&height=1024&seed={seed}&nologo=true"
                
                try:
                    img_res = requests.get(img_url, timeout=20)
                    if img_res.status_code == 200:
                        st.image(img_res.content, caption=f"بواسطة أحمد AI: {clean_p}")
                        st.download_button("📥 حفظ الصورة", img_res.content, "ahmed_ai_art.png", "image/png")
                        
                        # حفظ في الذاكرة
                        st.session_state.chat_history.append({"role": "user", "parts": [{"text": prompt}]})
                        st.session_state.chat_history.append({"role": "model", "parts": [{"text": f"تم رسم {clean_p}"}]})
                    else:
                        st.error("سيرفر الصور مشغول حالياً، حاول مرة ثانية.")
                except:
                    st.error("تعذر جلب الصورة من السيرفر.")
    else:
        # الرد النصي العادي
        with st.spinner("أحمد AI يفكر..."):
            res = ask_ahmed(prompt)
            with st.chat_message("assistant"):
                st.write(res)
            st.session_state.chat_history.append({"role": "user", "parts": [{"text": prompt}]})
            st.session_state.chat_history.append({"role": "model", "parts": [{"text": res}]})
