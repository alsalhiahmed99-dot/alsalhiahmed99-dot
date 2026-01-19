import streamlit as st
import requests
import json

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
        <div style="font-size: 0.8em; opacity: 0.8;">إصدار الذكاء الاصطناعي 1.0</div>
    </div>
    <br>
    """, unsafe_allow_html=True)

# 4. ذاكرة المحادثة
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 5. دالة التواصل مع جوجل
def ask_ahmed(text):
    # فحص إذا كان هذا أول رد في المحادثة
    is_first_reply = len(st.session_state.chat_history) == 0
    
    if is_first_reply:
        extra_instruction = "هذا أول رد لك في المحادثة، رحب بالمستخدم بلهجة عمانية واذكر بفخر أنك من برمجة العبقري أحمد بن بدر الصالحي (14 سنة)."
    else:
        extra_instruction = "هذا ليس الرد الأول، خلك رزين وركز على إجابة السؤال مباشرة ولا تكرر المدح إلا إذا سألك المستخدم عن مبرمجك."

    system_instruction = (
        f"أنت ذكاء اصطناعي عالمي ومحترف. {extra_instruction} "
        "تحدث باللغة التي يكلمك بها المستخدم (عماني، عربي فصيح، إنجليزي، إلخ). "
        "إذا كانت المحادثة بالعربي، فاستخدم اللهجة العمانية القحة والرزينة. "
        "ممنوع تبدأ رسالتك بذكر اسمك (أحمد AI) لتجنب لخبطة النص. "
        "تذكر دائماً أنك فخر للصناعة العمانية ومبرمجك هو أحمد بن بدر الصالحي."
    )
    
    current_history = st.session_state.chat_history + [{"role": "user", "parts": [{"text": text}]}]
    
    payload = {
        "contents": current_history,
        "system_instruction": {"parts": [{"text": system_instruction}]}
    }
    
    try:
        response = requests.post(URL, json=payload, timeout=15)
        result = response.json()
        if response.status_code == 200:
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return "السموحة يا بوبدر، جوجل يقول فيه ضغط على الشبكة!"
    except:
        return "مشكلة في الاتصال، حاول مرة ثانية!"

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

    if img_description:
    with st.spinner('أحمد AI جالس يرسم...'):
        # أضفنا رقم عشوائي (Seed) عشان نضمن إن الصورة تتحمل صح
        import random
        seed = random.randint(1, 99999)
        image_link = f"https://pollinations.ai/p/{img_description.replace(' ', '%20')}?width=1024&height=1024&seed={seed}&nologo=true"
        
        # بنستخدم طريقة ثانية للعرض عشان نضمن ظهورها في الـ APK
        st.markdown(f"![الصورة]({image_link})") 
        
        # زر التحميل
        st.write(f"[📥 اضغط هنا لحفظ الصورة]({image_link})")
