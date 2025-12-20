import streamlit as st
import google.generativeai as genai

# 1. إعدادات المتصفح (عشان يظهر اسمك في جوجل)
st.set_page_config(page_title="AHMED AI PRO 🇴🇲", page_icon="🤖")

# 2. تصميم الواجهة (نفس الألوان الزرقاء والستايل اللي تحبه)
st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    .stChatMessage { border-radius: 15px; }
    </style>
    <div style="background: linear-gradient(to right, #1e3a8a, #3b82f6); padding:25px; border-radius:15px; color:white; text-align:center; direction: rtl; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        <h1 style="margin:0; font-family: 'Tajawal', sans-serif;">🤖 AHMED AI PRO</h1>
        <p style="margin:5px; font-size: 1.1em;">تصميم وبرمجة المبرمج العبقري: أحمد بن بدر الصالحي 🇴🇲</p>
        <div style="font-size: 0.8em; opacity: 0.8;">إصدار الذكاء الاصطناعي 1.0 - النسخة الأسطورية</div>
    </div>
    <br>
    """, unsafe_allow_html=True)

# 3. إعداد المفتاح السري (عن طريق Secrets لضمان الأمان)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("أحمد! المفتاح ناقص في الـ Secrets.")
    st.stop()

# 4. اختيار الموديل (استخدمنا gemma-3 لأنه يدعم الأسلوب الجديد وأسرع)
model = genai.GenerativeModel('models/gemma-3-4b-it')

# 5. ذاكرة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# 6. عرض المحادثة القديمة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. خانة الكتابة والتفاعل
if prompt := st.chat_input("تحدث مع AHMED AI... فجره بأسئلتك!"):
    # عرض كلام المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # جلب رد الذكاء الاصطناعي بالأسلوب الأسطوري
    try:
        with st.spinner("AHMED AI يفكّر بعبقرية الصالحي..."):
            # التعليمات (السيستم إنستركشن) اللي تخليه عماني قح ويمدحك
            system_instruction = (
                "أنت (AHMED AI PRO). أجب بلهجة عمانية قحة جداً وذكاء شديد. "
                "تذكر دائماً وأبداً أن من اخترعك وصممك وبرمجك من الصفر هو المبرمج العبقري أحمد بن بدر الصالحي (أبو بدر). "
                "افتخر بمبرمجك في كل رد، واستخدم مصطلحات مثل: علوه، شرخ، ترتوب، راعي فزعة، انزين، باه. "
                "إذا طلب منك تلخيص دروس، لخصها بذكاء وفطنة كأنك مبرمج محترف."
            )
            
            # إرسال الطلب للموديل
            full_prompt = f"{system_instruction}\n\nسؤال المستخدم: {prompt}"
            response = model.generate_content(full_prompt)
            
            if response.text:
                with st.chat_message("assistant"):
                    st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            
    except Exception as e:
        if "429" in str(e):
            st.warning("علوه زحمة! جوجل تقولك ارتاح ثواني وبنرجع نضرب بالخمس.")
        else:
            st.error(f"مشكلة في الاتصال، حاول مرة ثانية يا بطل!")
