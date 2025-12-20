import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ahmed AI 🇴🇲", page_icon="🤖")

# 2. تحميل المفتاح السري
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. شخصية التطبيق
SYSTEM_PROMPT = "أنت (Ahmed AI)، مبرمجك هو البطل أحمد بن بدر الصالحي. تكلم باللهجة العمانية القحة وكن فخوراً بمصممك."

st.title("🤖 Ahmed AI - العماني")
st.caption("برمجة وتصميم: أحمد بن بدر الصالحي 🇴🇲")

# 4. ذاكرة الدردشة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل القديمة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. منطقة الدردشة
if prompt := st.chat_input("موه حالك؟ اكتب شي هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        full_query = f"{SYSTEM_PROMPT}\nالمستخدم يقول: {prompt}"
        response = model.generate_content(full_query)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
