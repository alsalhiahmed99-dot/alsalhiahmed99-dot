import streamlit as st
import google.generativeai as genai

# 1. إعداد واجهة الصفحة
st.set_page_config(page_title="Ahmed AI 🇴🇲", page_icon="🤖")

# إضافة صورة أو أيقونة وترحيب في البداية
st.title("🤖 Ahmed AI - النسخة العمانية")
st.markdown(f"### مرحباً بك! معكم الذكاء الاصطناعي الخاص بالمبرمج **أحمد الصالحي**")
st.caption("أنا هنا لأخدمك بلهجتنا العمانية الطيبة 🇴🇲")
st.markdown("---")

# 2. إعداد المفتاح السري
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("المفتاح غير موجود في Secrets!")
    st.stop()

# 3. اختيار الموديل (استخدمنا Gemma لأنه أثبت نجاحه معك الحين)
model = genai.GenerativeModel('models/gemma-3-4b-it')

# 4. إدارة ذاكرة المحادثة
if "messages" not in st.session_state:
    # رسالة ترحيبية تظهر في بداية المحادثة تلقائياً
    st.session_state.messages = [
        {"role": "assistant", "content": "حيّاك الله الغالي! أنا أحمد AI، كيف أقدر أساعدك اليوم؟ تفضل هود هود.."}
    ]

# عرض الرسائل المخزنة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. منطقة الإدخال والتفاعل
if prompt :=
