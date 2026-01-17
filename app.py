import streamlit as st
import requests
import json

# 1. إعدادات المتصفح
st.set_page_config(page_title="أحمد AI PRO", page_icon="🤖")

# 2. مفاتيح التشغيل (المفتاح السري من Streamlit Secrets)
MY_KEY = st.secrets["GOOGLE_API_KEY"]
MODEL_NAME = "gemini-1.5-flash" 
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={MY_KEY}"

# 3. تصميم الواجهة وتعديل اتجاه النص (عشان ما يظهر مقلوب)
st.markdown("""
    <style>
    /* جعل الصفحة تدعم اللغة العربية من اليمين لليسار */
    .main { background-color: #0b0e14; direction: rtl; }
    .stChatMessage { border-radius: 15px; direction: rtl; text-align: right; }
    
    /* تنسيق محتوى الرسائل ليكون من اليمين */
    div[data-testid="stChatMessageContent"] {
        direction: rtl;
        text-align: right;
    }
    
    /* تنسيق صندوق الإدخال */
    input {
        direction: rtl;
        text-align: right;
    }
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
    system_instruction = (
        "أجب بلهجة عمانية قحة. "
        "ممنوع منعاً باتاً أن تضع اسمك في بداية الرد (مثل: أحمد AI: ...)؛ ابدأ كلامك مباشرة. "
        "إذا سألك أحد عن اسمك أو من أنت، أجب بأنك 'أحمد AI' وأن مبرمجك ومخترعك هو العبقري أحمد بن بدر الصالحي. "
        "افتخر بمبرمجك وإنجازه وعمره (14 سنة) في ثنايا كلامك بشكل طبيعي جداً."
    )
    
    current_history = []
    for msg in st.session_state.chat_history:
        current_history.append({"role": msg["role"], "parts": [{"text": msg["parts"][0]["text"]}]})
    
    current_history.append({"role": "user", "parts": [{"text": text}]})
    
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
            return "السموحة يا بوبدر، جوجل يقول فيه ضغط على الشبكة حالياً!"
    except:
        return "مشكلة في الاتصال، حاول مرة ثانية!"

# 6. عرض الشات
for message in st.session_state.chat_history:
    role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(role):
        st.write(message["parts"][0]["text"])

# 7. خانة الكتابة
if prompt := st.chat_input("تحدث مع أحمد AI..."):
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.spinner("أحمد AI يفكر..."):
        res = ask_ahmed(prompt)
    
    with st.chat_message("assistant"):
        st.write(res)
    
    st.session_state.chat_history.append({"role": "user", "parts": [{"text": prompt}]})
    st.session_state.chat_history.append({"role": "model", "parts": [{"text": res}]})
