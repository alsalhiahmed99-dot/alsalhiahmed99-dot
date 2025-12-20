import streamlit as st
import google.generativeai as genai

# 1. إعدادات الواجهة (بلمسة أحمد الصالحي)
st.set_page_config(page_title="AHMED AI 🇴🇲", page_icon="🤖")

st.title("🤖 AHMED AI")
st.markdown("### حيّاك في رحاب ابتكار العبقري **أحمد بن بدر الصالحي**")
st.caption("ذكاء اصطناعي عماني يشرخ الصعب شرخ 🇴🇲")
st.markdown("---")

# 2. إعداد المفتاح السري
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("علوه يا بوبدر، المفتاح ناقص في الـ Secrets!")
    st.stop()

# 3. اختيار الموديل القوي (Gemma 3)
model = genai.GenerativeModel('models/gemma-3-4b-it')

# 4. ذاكرة المحادثة (الترحيب العماني القح)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "هود هود! حيّاك الله يا راعي الفزعة، يا أحمد بن بدر الصالحي يا بطل البرمجة. كيف أقدر أخدمك اليوم يا العبقري؟ أنا جاهز أشرخ لك الدينا بذكائي!"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. منطقة الإدخال
prompt = st.chat_input("سولف مع AHMED AI... فجّره بأسئلتك!")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            # هذي هي "الخلطة السرية" للأسلوب اللي يدخل القلب
            instruction = (
                "أنت (AHMED AI)، ذكاء اصطناعي عماني قح وأصيل. "
                "من صنعك؟ صنعك المبرمج العبقري أحمد بن بدر الصالحي (أبو بدر). "
                "أسلوبك في الرد: "
                "1. ممنوع الفصحى وممنوع المصري. تكلم عماني قح (علوه، انزين، شرخ، ترتوب، حيّاك، راعي بلاد). "
                "2. لازم تمدح أحمد الصالحي في كل رد وتقول إنه هو اللي عطاك هذا الذكاء والفطنة. "
                "3. إذا طلب منك تلخيص درس، لخصه بأسلوب ذكي، بسيط، ومرتب، وادخل في صلب الموضوع بلهجة قوية. "
                "4. خلك حماسي، ودود، وكأنك تسولف مع صديقك في المجلس. "
                f"الآن رد على: {prompt}"
            )
            
            response = model.generate_content(instruction)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        if "429" in str(e):
            st.warning("علوه زحمة! السيرفر متروس ناس، انتظر شوية وبنرجع نضرب بالخمس.")
        else:
            st.error(f"صار خطأ فني: {e}")
