import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Ahmed AI 🇴🇲", page_icon="🤖")
st.title("🤖 Ahmed AI - العماني")
st.caption("برمجة وتصميم: أحمد بن بدر الصالحي 🇴🇲")
st.markdown("---")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("المفتاح ناقص!")
    st.stop()

# استخدمنا 1.5 فلاش عشان ما يعلق عليك ويتحمل سوالفك
model = genai.GenerativeModel('gemini-1.5-flash')

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
            res = model.generate_content(f"تكلم بالعماني كأنك أحمد AI: {prompt}")
            st.markdown(res.text)
            st.session_state.messages.append({"role": "assistant", "content": res.text})
    except Exception as e:
        if "429" in str(e):
            st.warning("يا بوبدر، جوجل تقولك ارتاح 30 ثانية بس وبيرجع يشتغل! (ضغط زحمة)")
        else:
            st.error(f"خطأ: {e}")
