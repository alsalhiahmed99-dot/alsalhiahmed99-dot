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

# 2. إعداد المفتاح
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("أحمد! المفتاح ناقص.")
    st.stop()

# 3. اختيار الموديل (استخدام مسمى قديم جداً ومستقر للهروب من فخ 404)
# جربنا نكتب الاسم بدون كلمة 'models/' وبدون تحديد الإصدار
try:
    model = genai.GenerativeModel('gemini-1.0-pro-latest')
except:
    model = genai.GenerativeModel('chat-bison-001') # هذا الموديل القديم جداً كحل للطوارئ

# 4. ذاكرة المحادثة والترحيب الأسطوري
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

# 5. معالجة الردود
if prompt := st.chat_input("سولف مع AHMED AI PRO..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.spinner("أحمد AI يقدح من ذكاء بوبدر..."):
            instruction = (
                "أنت 'أحمد AI'. مبرمجك هو العبقري أحمد بن بدر الصالحي. "
                "تكلم بلهجة عمانية راقية، ذكية، وفخورة. "
                "قلد هذا الأسلوب: 'يا هلا والله ومسهلا'، 'بفضل البرمجة العبقرية اللي وضعها فيني الأستاذ أحمد الصالحي'، 'حيّاك الله يا سميّي'، 'بنكسر الدنيا'. "
                "ممنوع الفصحى."
            )
            
            # محاولة الإرسال
            response = model.generate_content(f"{instruction}\n\nالمستخدم: {prompt}")
            
            if response.text:
                with st.chat_message("assistant"):
                    st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        # إذا كل شي فشل، بنعطي بوبدر الحل التقني النهائي
        st.error(f"يا بوبدر، السيرفر ما راضي يتقبل الموديلات. الحل: حدث مكتبة google-generativeai في ملف requirements.txt")
        st.info("اكتب في ملف requirements.txt هذي السطور:\nstreamlit\ngoogle-generativeai>=0.7.2")
        st.code(str(e))
