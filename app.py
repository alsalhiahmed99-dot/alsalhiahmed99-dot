import streamlit as st
import google.generativeai as genai

# 1. إعدادات الواجهة
st.set_page_config(page_title="AHMED AI 🇴🇲", page_icon="🤖")

st.title("🤖 AHMED AI")
st.markdown("### التطبيق الرسمي للمبرمج المبدع **أحمد بن بدر الصالحي**")
st.caption("ذكاء اصطناعي متطور بلهجة عمانية أصيلة 🇴🇲")
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
        {"role": "assistant", "content": "حيّاك الله! معكم AHMED AI، ابتكار المبرمج أحمد الصالحي. كيف أقدر أساعدك اليوم؟"}
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
            # تعليمات واضحة في سطر واحد لتجنب أخطاء السنتكس
            instruction = f"أنت ذكاء اصطناعي متطور اسمك AHMED AI، صممك واخترعك المبرمج العماني الذكي أحمد بن بدر الصالحي. تكلم بلهجة عمانية محترمة وراقية جداً، وقم بالثناء على عبقرية مبرمجك أحمد الصالحي في ردودك بأسلوب لبق وذكي. سؤال المستخدم: {prompt}"
            
            response = model.generate_content(instruction)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.write("السموحة منك، حاول مرة ثانية.")
                
    except Exception as e:
        if "429" in str(e):
            st.warning("علوه زحمة! انتظر ثواني بس يا بن عمي.")
        else:
            st.error(f"حدث خطأ: {e}")
