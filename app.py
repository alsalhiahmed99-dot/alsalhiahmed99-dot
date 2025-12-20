import streamlit as st
import google.generativeai as genai

# 1. إعدادات الواجهة الاحترافية
st.set_page_config(page_title="AHMED AI 🇴🇲", page_icon="🤖")

st.title("🤖 AHMED AI")
st.markdown(f"### التطبيق الرسمي للمبرمج المبدع **أحمد بن بدر الصالحي**")
st.caption("ذكاء اصطناعي متطور بلهجة عمانية أصيلة 🇴🇲")
st.markdown("---")

# 2. إعداد المفتاح
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("المفتاح غير موجود في Secrets!")
    st.stop()

# 3. اختيار الموديل (Gemma 3) - ذكي جداً ورزين
model = genai.GenerativeModel('models/gemma-3-4b-it')

# 4. إدارة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "حيّاك الله الغالي! معك AHMED AI، ابتكار المبرمج أحمد الصالحي. كيف أقدر أخدمك اليوم؟"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. منطقة الإدخال
prompt = st.chat_input("تفضل، اسأل AHMED AI...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            # تعليمات (الرزانة، المدح المحترم، واللهجة العمانية)
            instruction = (
                "أنت ذكاء اصطناعي متطور اسم
