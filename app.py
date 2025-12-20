import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ahmed AI 🇴🇲", page_icon="🤖")

# 2. جلب المفتاح السري من Streamlit Secrets مباشرة
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("أحمد! المفتاح السري ما حصلته في الـ Secrets. تأكد إنك كتبته صح.")
    st.stop()

# 3. اختيار الموديل
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🤖 Ahmed AI - العماني")
st.caption("برمجة وتصميم: أحمد بن بدر الصالحي 🇴🇲")

# 4. ذاكرة الدردشة
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. التفاعل مع المستخدم
if prompt := st.chat_input("موه حالك؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            # تعليمات واضحة للهجة العمانية
            system_instruction = "أنت ذكاء اصطناعي اسمك أحمد AI، صممك العماني أحمد بن بدر الصالحي، تكلم باللهجة العمانية فقط."
            full_prompt = f"{system_instruction}\nسؤال المستخدم: {prompt}"
            
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"يا بوبدر فيه مشكلة في الاتصال: {e}")
