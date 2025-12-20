import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Ahmed AI 🇴🇲", page_icon="🤖")

# التأكد من المفتاح
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("المفتاح غير موجود في Secrets!")
    st.stop()

# محاولة تشغيل الموديل المتوفر
try:
    # جربنا Pro لأنه الأكثر ضماناً
    model = genai.GenerativeModel('gemini-1.5-pro')
except:
    model = genai.GenerativeModel('gemini-pro')

st.title("🤖 Ahmed AI - العماني")
st.caption("برمجة وتصميم: أحمد بن بدر الصالحي 🇴🇲")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("موه حالك؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            # تعليمات واضحة
            res = model.generate_content(f"تكلم بالعماني: {prompt}")
            st.markdown(res.text)
            st.session_state.messages.append({"role": "assistant", "content": res.text})
    except Exception as e:
        st.error(f"يا أحمد، هذا هو الخطأ: {e}")
        st.info("جرب تغير اسم الموديل في الكود إلى 'gemini-pro' فقط.")
