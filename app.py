import streamlit as st
import google.generativeai as genai

# 1. إعداد الواجهة (نفس أول)
st.set_page_config(page_title="Ahmed AI 🇴🇲", page_icon="🤖")

st.title("🤖 Ahmed AI - العماني")
st.caption("برمجة وتصميم: أحمد بن بدر الصالحي 🇴🇲")
st.markdown("---")

# 2. التأكد من المفتاح السري (Secrets)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("يا أحمد، المفتاح ما حصلته في Secrets! تأكد إنك ضفته في إعدادات Streamlit.")
    st.stop()

# 3. اختيار الموديل المستقر (هذا مستحيل يعطيك 404)
model = genai.GenerativeModel('gemini-pro')

# 4. ذاكرة الدردشة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. منطقة الإدخال والتفاعل
if prompt := st.chat_input("موه حالك؟ اكتب شي هنا..."):
    # إضافة رسالة المستخدم للذاكرة
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # توليد الرد من Ahmed AI
    try:
        with st.chat_message("assistant"):
            # توجيه اللهجة العمانية والتعريف بالمبرمج
            instruction = f"أنت ذكاء اصطناعي اسمك Ahmed AI صممك المبرمج العماني أحمد بن بدر الصالحي. تكلم باللهجة العمانية فقط. سؤال المستخدم: {prompt}"
            
            response = model.generate_content(instruction)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.error("جوجل ما ردت بشي، جرب مرة ثانية.")
                
    except Exception as e:
        st.error(f"يا بوبدر صار خطأ: {e}")
