import streamlit as st
import google.generativeai as genai

# إعداد الواجهة الجميلة مالك
st.set_page_config(page_title="Ahmed AI 🇴🇲", page_icon="🤖")
st.title("🤖 Ahmed AI - العماني")
st.caption("برمجة وتصميم: أحمد بن بدر الصالحي 🇴🇲")
st.markdown("---")

# التأكد من المفتاح
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("أحمد، المفتاح ما موجود في Secrets!")
    st.stop()

# السر هنا: اخترنا موديل 2.0-flash-lite لأنه سريع وما يزعل بسرعة
model = genai.GenerativeModel('models/gemini-2.0-flash-lite-preview-02-05')

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
            # إرسال الطلب
            response = model.generate_content(f"أنت أحمد AI، تكلم بالعماني: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        if "429" in str(e):
            st.warning("يا أحمد، السيرفر عليه زحمة، انتظر 20 ثانية وجرب مرة ثانية.")
        else:
            st.error(f"صار خطأ: {e}")
