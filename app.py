import streamlit as st
import google.generativeai as genai

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

# 3. اختيار الموديل (استخدمنا الاسم المباشر عشان نتفادى خطأ 404)
# هذا الاسم يشتغل مع النسخة المستقرة v1
model = genai.GenerativeModel('gemini-pro')

# 4. الذاكرة
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
            # طلب الرد بأبسط طريقة ممكنة
            response = model.generate_content(f"تكلم بالعماني: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        # إذا استمر الخطأ، بنخلي البرنامج يخبرنا شو هي الموديلات المتاحة لحسابك بالضبط
        st.error("أحمد، حسابك يحتاج موديل محدد. هذي هي الموديلات اللي تقدر تستخدمها:")
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        st.write(available_models)
