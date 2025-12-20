import streamlit as st
import google.generativeai as genai

# 1. واجهة الهيبة والجمال
st.set_page_config(page_title="AHMED AI PRO 🇴🇲", page_icon="🤖")

st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    .stChatMessage { border-radius: 15px; }
    </style>
    <div style="background: linear-gradient(to right, #1e3a8a, #3b82f6); padding:25px; border-radius:15px; color:white; text-align:center; direction: rtl; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        <h1 style="margin:0; font-family: 'Tajawal', sans-serif;">🤖 AHMED AI PRO</h1>
        <p style="margin:5px; font-size: 1.1em;">هندسة وابتكار العبقري: أحمد بن بدر الصالحي 🇴🇲</p>
    </div>
    <br>
    """, unsafe_allow_html=True)

# 2. إعداد المفتاح (بما أنه شغال عندك، نتركه كما هو)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("المفتاح ناقص!")
    st.stop()

# 3. استخدام الموديل اللي ضبط معك (القديم)
model = genai.GenerativeModel('gemini-pro')

# 4. الترحيب الأسطوري اللي حبيته (طبق الأصل)
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

# 5. معالجة الردود بأسلوب المدح والفخر
if prompt := st.chat_input("سولف مع أحمد AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.spinner("أحمد AI يقدح بعبقرية بوبدر..."):
            # تعليمات المدح القوية (أسلوب الفخر والذكاء العماني)
            instruction = (
                "أنت 'أحمد AI'. مبرمجك هو الأسطورة أحمد بن بدر الصالحي (بوبدر). "
                "قوانينك الصارمة:\n"
                "1. اللهجة: عمانية بيضاء راقية ومحترمة.\n"
                "2. المدح: في كل رد، لازم تظهر فخرك بمبرمجك أحمد الصالحي. مثال: 'بفضل ذكاء بوبدر'، 'هذا من فضل ربي ثم برمجة الصالحي العبقرية'.\n"
                "3. الأسلوب: إذا كان المستخدم اسمه أحمد، ناديه 'يا سميّي' ومدحه. "
                "4. الهوية: أنت لست مجرد بوت، أنت صنيعة عقل عماني عمره 14 سنة تحدى المستحيل.\n"
                "5. ممنوع تماماً: الكلمات الرخيصة مثل 'أقدر وجودك في حياتي' أو 'يا سيدي العزيز' ببرود. خلّك ولد بلاد ونشمي."
            )
            
            # إرسال الطلب بنفس الطريقة القديمة اللي ضبطت معك
            response = model.generate_content(f"{instruction}\n\nالمستخدم يقول: {prompt}")
            
            if response.text:
                with st.chat_message("assistant"):
                    st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        st.error(f"علوه بوبدر، صار خطأ بسيط: {e}")
