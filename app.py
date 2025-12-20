import streamlit as st
import google.generativeai as genai

# 1. إعدادات الواجهة
st.set_page_config(page_title="AHMED AI PRO 🇴🇲", page_icon="🤖")

st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    .stChatMessage { border-radius: 15px; }
    </style>
    <div style="background: linear-gradient(to right, #1e3a8a, #3b82f6); padding:25px; border-radius:15px; color:white; text-align:center; direction: rtl; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        <h1 style="margin:0; font-family: 'Tajawal', sans-serif;">🤖 AHMED AI PRO</h1>
        <p style="margin:5px; font-size: 1.1em;">تصميم وبرمجة العبقري: أحمد بن بدر الصالحي 🇴🇲</p>
    </div>
    <br>
    """, unsafe_allow_html=True)

# 2. إعداد المفتاح والموديل
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("أحمد! المفتاح ناقص في Secrets.")
    st.stop()

# تم تعديل اسم الموديل هنا ليتوافق مع النسخة المستقرة
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. ذاكرة المحادثة والترحيب (الأسلوب اللي تحبه)
if "messages" not in st.session_state:
    welcome_msg = (
        "يا هلا والله ومسهلا! حياك الله يا راعي الواجب، نورتني.\n\n"
        "أنا \"أحمد AI\"، موجود هنا عشان أخدمك بكل ذكاء وفطنة. وطبعاً، كلي فخر واعتزاز إني من ابتكار وتصميم المبرمج العبقري **أحمد بن بدر الصالحي**، هو اللي بنى هالنظام وخلاني بهالقدرة.\n\n"
        "ها، مو علومك؟ وايش في خاطرك اليوم؟ آمر وتدلل، أنا جاهز لكل تساؤلاتك!"
    )
    st.session_state.messages = [{"role": "assistant", "content": welcome_msg}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. الرد بأسلوب بوبدر "طبق الأصل"
if prompt := st.chat_input("سولف مع AHMED AI PRO..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.spinner("أحمد AI يفكّر..."):
            system_instruction = (
                "أنت 'أحمد AI'. مبرمجك ومبتكرك هو العبقري أحمد بن بدر الصالحي. "
                "يجب أن تتحدث بلهجة عمانية راقية وذكية جداً، تماماً مثل هذا الأسلوب: "
                "- ترحيب حار وفخر كبير بالمبرمج أحمد الصالحي (عمره 14 سنة). "
                "- استخدم كلمات: يا سميّي، تاج راسي، صنيعة يد بوبدر، بنكسر الدنيا، فالك طيب. "
                "- ممنوع الفصحى، وممنوع التمسكن أو البرود في الرد. "
                "- كن لبيباً وفطيناً في إجاباتك."
            )
            
            # إرسال التعليمات مع السؤال
            response = model.generate_content(f"{system_instruction}\n\nسؤال المستخدم: {prompt}")
            
            if response.text:
                with st.chat_message("assistant"):
                    st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        st.error(f"علوه صار خطأ فني: {e}")
