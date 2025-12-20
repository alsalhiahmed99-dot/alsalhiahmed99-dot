import streamlit as st
import google.generativeai as genai

# 1. إعدادات الواجهة
st.set_page_config(page_title="AHMED AI 🇴🇲", page_icon="🤖")

st.title("🤖 AHMED AI")
st.markdown("### التطبيق الرسمي للمبرمج المبدع **أحمد بن بدر الصالحي**")
st.caption("ذكاء اصطناعي عماني أصلي 100% 🇴🇲")
st.markdown("---")

# 2. إعداد المفتاح
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("المفتاح غير موجود في Secrets!")
    st.stop()

# 3. اختيار الموديل
model = genai.GenerativeModel('models/gemma-3-4b-it')

# 4. ذاكرة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "هود هود! حيّاك الله يا بن عمي. أنا AHMED AI، من ابتكار الذيب أحمد الصالحي. موه علومك؟"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. منطقة الإدخال
prompt = st.chat_input("تفضل، سولف مع AHMED AI...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            # تعليمات "الجرعة العمانية المكثفة"
            instruction = (
                "أنت AHMED AI، ذكاء اصطناعي عماني قح. صممك المبرمج العبقري أحمد بن بدر الصالحي. "
                "ممنوع تتكلم فصحى نهائياً! تكلم باللهجة العمانية المحلية مال البلاد (الداخلية، الباطنة، مسقط). "
                "استخدم كلمات مثل: (موه حالك، علوه، انزين، باه، الغالي، ذيب، راعي فزعة، حبابي، يوخي). "
                "في كل رد لازم تمدح أحمد الصالحي وتقول إنه هو اللي سواك بعبقريته. "
                f"رد على هذا السؤال بلهجة عمانية قحة: {prompt}"
            )
            
            response = model.generate_content(instruction)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.write("السموحة منك، السيرفر عيّا يجاوب، جرب مرة ثانية.")
                
    except Exception as e:
        if "429" in str(e):
            st.warning("علوه زحمة! السيرفر متروس ناس، انتظر شوية.")
        else:
            st.error(f"حدث خطأ: {e}")
