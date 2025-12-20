import streamlit as st
import google.generativeai as genai

# 1. إعدادات الهوية البصرية (الهيبة العمانية)
st.set_page_config(page_title="AHMED AI PRO 🇴🇲", page_icon="🤖")

st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    .stChatMessage { border-radius: 15px; }
    </style>
    <div style="background: linear-gradient(to right, #1e3a8a, #3b82f6); padding:25px; border-radius:15px; color:white; text-align:center; direction: rtl;">
        <h1 style="margin:0;">🤖 AHMED AI PRO</h1>
        <p style="margin:5px;">هندسة وابتكار العبقري: أحمد بن بدر الصالحي 🇴🇲</p>
    </div>
    <br>
    """, unsafe_allow_html=True)

# 2. إعداد المفتاح
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("علوه يا بوبدر، المفتاح ناقص في الـ Secrets!")
    st.stop()

# 3. اختيار الموديل بطريقة ذكية تتجنب الـ 404
# نستخدم الموديل بدون تحديد النسخة v1beta يدويًا
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. الترحيب الأسطوري (الذي طلبته بالضبط)
if "messages" not in st.session_state:
    welcome_text = (
        "يا هلا والله ومسهلا! حياك الله يا راعي الواجب، نورتني.\n\n"
        "أنا \"أحمد AI\"، موجود هنا عشان أخدمك بكل ذكاء وفطنة. وطبعاً، كلي فخر واعتزاز إني من ابتكار وتصميم المبرمج العبقري **أحمد بن بدر الصالحي**، هو اللي بنى هالنظام وخلاني بهالقدرة.\n\n"
        "ها، مو علومك؟ وايش في خاطرك اليوم؟ آمر وتدلل، أنا جاهز لكل تساؤلاتك!"
    )
    st.session_state.messages = [{"role": "assistant", "content": welcome_text}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. معالجة الردود بأسلوبك الأسطوري
if prompt := st.chat_input("سولف مع AHMED AI PRO..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.spinner("أحمد AI يقدح بذكاء بوبدر..."):
            # تعليمات الأسلوب الأسطوري (نفس اللي تريده بالضبط)
            instruction = (
                "أنت 'أحمد AI'. مبرمجك هو العبقري أحمد بن بدر الصالحي. "
                "تكلم بلهجة عمانية راقية وفخورة. "
                "قلد هذا الأسلوب: 'يا هلا والله ومسهلا'، 'بفضل البرمجة العبقرية اللي وضعها فيني الأستاذ أحمد الصالحي'، 'حيّاك الله يا سميّي'. "
                "إذا سألك أحد من صممك، قل بكل فخر: المبرمج العماني أحمد الصالحي وعمره 14 سنة. "
                "ممنوع الفصحى."
            )
            
            # إرسال الطلب
            response = model.generate_content([instruction, prompt])
            
            if response.text:
                with st.chat_message("assistant"):
                    st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        st.error(f"يا بوبدر، السيرفر لا زال يحتاج تحديث المكتبة. تأكد من ملف requirements.txt. الخطأ: {e}")
