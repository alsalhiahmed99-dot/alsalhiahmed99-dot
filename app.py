import streamlit as st
import google.generativeai as genai

# 1. إعداد الواجهة (نفس ما تحب)
st.set_page_config(page_title="Ahmed AI 🇴🇲", page_icon="🤖")
st.title("🤖 Ahmed AI - العماني")
st.caption("برمجة وتصميم: أحمد بن بدر الصالحي 🇴🇲")
st.markdown("---")

# 2. إعداد المفتاح
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("المفتاح غير موجود!")
    st.stop()

# 3. استخدام الموديل المتطور اللي طلع في قائمتك (رقم 3)
model = genai.GenerativeModel('models/gemini-2.0-flash')

# 4. ذاكرة الدردشة
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. التفاعل
if prompt := st.chat_input("موه حالك؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            # تعليمات للهجة العمانية
            full_prompt = f"أنت ذكاء اصطناعي اسمك أحمد AI، صممك أحمد بن بدر الصالحي. تكلم باللهجة العمانية فقط: {prompt}"
            
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"يا بوبدر صار خطأ بسيط: {e}")
