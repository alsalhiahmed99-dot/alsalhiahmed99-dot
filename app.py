import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة والواجهة
st.set_page_config(page_title="Ahmed AI 🇴🇲", page_icon="🤖")

st.title("🤖 Ahmed AI - العماني")
st.caption("برمجة وتصميم: أحمد بن بدر الصالحي 🇴🇲")
st.markdown("---")

# جلب المفتاح السري من Streamlit
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("أحمد! المفتاح السري ناقص في الـ Secrets. ضيفه عشان أقدر أتكلم.")
    st.stop()

# اختيار الموديل المستقر والسريع
model = genai.GenerativeModel('gemini-1.5-flash')

# ذاكرة الدردشة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# التفاعل مع المستخدم
if prompt := st.chat_input("موه حالك؟ اكتب شي هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            # التعليمات السرية لـ أحمد AI
            instruction = (
                "أنت ذكاء اصطناعي اسمك Ahmed AI. "
                "المبرمج العماني أحمد بن بدر الصالحي هو من اخترعك وصممك. "
                "تكلم باللهجة العمانية فقط بأسلوب ودي ومحترم. "
                f"سؤال المستخدم: {prompt}"
            )
            
            response = model.generate_content(instruction)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
    except Exception as e:
        st.error(f"يا بوبدر فيه مشكلة بسيطة: {e}")
