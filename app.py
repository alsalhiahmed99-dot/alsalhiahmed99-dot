import streamlit as st
import google.generativeai as genai

# 1. إعداد الواجهة (بسيطة وجميلة نفس أول)
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

# 3. محاولة تعريف الموديل بأكثر طريقة مباشرة
# شلنا كلمة models/ وشلنا الإصدارات التجريبية
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    model = genai.GenerativeModel('gemini-pro')

# 4. ذاكرة الدردشة
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. التفاعل
if prompt := st.chat_input("موه حالك؟ اكتب شي..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            # طلب الرد ببساطة بدون تعقيدات في الـ options
            response = model.generate_content(f"تكلم باللهجة العمانية بصفتك أحمد AI: {prompt}")
            
            if response:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"يا أحمد، صار خطأ في النظام: {e}")
        st.info("تأكد إن مفتاح الـ API شغال وما منتهي صلاحيته من Google AI Studio.")
