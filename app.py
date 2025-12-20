import streamlit as st
import google.generativeai as genai

# 1. إعداد الواجهة (نفس أول - بسيطة وجميلة)
st.set_page_config(page_title="Ahmed AI 🇴🇲", page_icon="🤖")
st.title("🤖 Ahmed AI - العماني")
st.caption("برمجة وتصميم: أحمد بن بدر الصالحي 🇴🇲")
st.markdown("---")

# 2. جلب المفتاح
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("المفتاح غير موجود!")
    st.stop()

# 3. اختيار الموديل المستقر (بدون أرقام إصدارات معقدة)
# جربنا 'gemini-pro' لأنه يقبل الاتصال العادي (v1)
model = genai.GenerativeModel('gemini-pro')

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
            # تعليمات واضحة
            full_query = f"أنت ذكاء اصطناعي اسمك أحمد AI. تكلم باللهجة العمانية فقط. سؤال المستخدم: {prompt}"
            
            # الطلب البسيط
            response = model.generate_content(full_query)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        # إذا صار خطأ، بيخبرنا بالضبط شو نوعه
        st.error(f"يا بوبدر، جوجل تقول: {e}")
