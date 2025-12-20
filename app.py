import streamlit as st
import google.generativeai as genai

# 1. إعداد واجهة الصفحة
st.set_page_config(page_title="Ahmed AI 🇴🇲", page_icon="🤖")

st.title("🤖 Ahmed AI - النسخة العمانية")
st.markdown("### مرحباً بك! معكم الذكاء الاصطناعي الخاص بالمبرمج **أحمد الصالحي**")
st.caption("أنا هنا لأخدمك بلهجتنا العمانية الطيبة 🇴🇲")
st.markdown("---")

# 2. إعداد المفتاح السري
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("المفتاح غير موجود في Secrets!")
    st.stop()

# 3. اختيار الموديل (Gemma-3-4b-it)
model = genai.GenerativeModel('models/gemma-3-4b-it')

# 4. إدارة ذاكرة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "حيّاك الله الغالي! أنا أحمد AI، كيف أقدر أساعدك اليوم؟ تفضل هود هود.."}
    ]

# عرض الرسائل المخزنة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. منطقة الإدخال والتفاعل (تأكد من كتابة هذا السطر كاملاً)
prompt = st.chat_input("اكتب سؤالك هنا يا بطل...")

if prompt:
    # إضافة رسالة المستخدم للذاكرة
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            # تعليمات اللهجة والتعريف بالمبرمج
            instruction = (
                f"أنت ذكاء اصطناعي اسمك (أحمد AI). مبرمجك ومخترعك هو (أحمد بن بدر الصالحي). "
                f"تكلم بلهجة عمانية قحة ومحببة. سؤال المستخدم: {prompt}"
            )
            
            response = model.generate_content(instruction)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.write("السموحة منك، ما جاني رد، جرب مرة ثانية.")
                
    except Exception as e:
        if "429" in str(e):
            st.warning("علوه زحمة! انتظر ثواني وجرب مرة ثانية.")
        else:
            st.error(f"صار خطأ: {e}")
