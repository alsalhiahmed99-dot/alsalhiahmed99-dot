import streamlit as st
import google.generativeai as genai
from google.generativeai.types import RequestOptions

# 1. إعداد الواجهة
st.set_page_config(page_title="Ahmed AI 🇴🇲", page_icon="🤖")
st.title("🤖 Ahmed AI - العماني")
st.caption("برمجة وتصميم: أحمد بن بدر الصالحي 🇴🇲")
st.markdown("---")

# 2. إعداد المفتاح
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("المفتاح غير موجود في Secrets!")
    st.stop()

# 3. اختيار الموديل مع إجبار نسخة API v1 (هذا هو الحل للـ 404)
model = genai.GenerativeModel('gemini-1.5-flash')

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
            # إجبار الطلب على استخدام نسخة v1 بدلاً من v1beta
            response = model.generate_content(
                f"تكلم باللهجة العمانية بصفتك أحمد AI: {prompt}",
                request_options=RequestOptions(api_version='v1')
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        # إذا فشل Flash، بنجرب Pro كخيار أخير وبنفس الطريقة
        try:
            model_pro = genai.GenerativeModel('gemini-pro')
            response = model_pro.generate_content(
                f"تكلم باللهجة العمانية بصفتك أحمد AI: {prompt}",
                request_options=RequestOptions(api_version='v1')
            )
            st.markdown(response.text)
        except Exception as e2:
            st.error(f"يا بوبدر، جوجل تقول: {e2}")
