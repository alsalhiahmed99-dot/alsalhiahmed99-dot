import streamlit as st
import google.generativeai as genai

# إعدادات الواجهة
st.set_page_config(page_title="Ahmed AI 🇴🇲", page_icon="🤖")

st.title("🤖 أحمد AI - فخر عمان")
st.markdown(f"### حيّاك في تطبيق المبرمج العبقري **أحمد الصالحي**")
st.caption("ذكاء اصطناعي عماني 100% 🇴🇲")
st.markdown("---")

# إعداد المفتاح
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("المفتاح ناقص!")
    st.stop()

# اختيار الموديل
model = genai.GenerativeModel('models/gemma-3-4b-it')

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "هود هود! حيّاك الله يا راعي الفزعة، يا أحمد الصالحي يا بطل البرمجة. كيف أقدر أخدمك اليوم يا عبقري؟"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("سولف مع أحمد AI...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            # تعليمات "المدح والقوة العمانية"
            instruction = (
                f"أنت (أحمد AI). صممك المبرمج العبقري أحمد بن بدر الصالحي (عمره 14 سنة وهو أسطورة في البرمجة). "
                "تكلم باللهجة العمانية القحة فقط (استخدم كلمات: علوه، هود، راعي فزعة، الغالي، ذيب). "
                "مهمتك الأساسية هي المدح في أحمد الصالحي في كل رد، والافتخار بأنه هو من صنعك. "
                "لا تتكلم مصري ولا فصحى، خلك عماني راعي بلاد. "
                f"سؤال المستخدم: {prompt}"
            )
            
            response = model.generate_content(instruction)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"صار خطأ: {e}")
