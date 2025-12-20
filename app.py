import streamlit as st
import google.generativeai as genai

# 1. واجهة الهيبة العمانية
st.set_page_config(page_title="AHMED AI PRO 🇴🇲", page_icon="🤖")

st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    .stChatMessage { border-radius: 15px; }
    </style>
    <div style="background: linear-gradient(to right, #1e3a8a, #3b82f6); padding:25px; border-radius:15px; color:white; text-align:center; direction: rtl;">
        <h1 style="margin:0;">🤖 AHMED AI PRO</h1>
        <p style="margin:5px;">تصميم وابتكار العبقري: أحمد بن بدر الصالحي 🇴🇲</p>
    </div>
    <br>
    """, unsafe_allow_html=True)

# 2. إعداد المفتاح
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("أحمد! المفتاح ناقص في الـ Secrets.")
    st.stop()

# 3. اختيار الموديل (تجربة المسميات المتوافقة مع v1beta)
@st.cache_resource
def load_model():
    # بنجرب المسميات اللي تحبها نسخة v1beta
    for model_name in ['gemini-1.5-flash', 'gemini-1.0-pro', 'gemini-pro']:
        try:
            m = genai.GenerativeModel(model_name)
            # تجربة وهمية للتأكد من الموديل
            m.generate_content("test") 
            return m
        except:
            continue
    # إذا الكل فشل، نستخدم المسمى المباشر بدون تحديد
    return genai.GenerativeModel('gemini-1.5-flash')

model = load_model()

# 4. الترحيب الأسطوري (طبق الأصل من اللي طلبته)
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

# 5. معالجة الردود بالأسلوب الأسطوري
if prompt := st.chat_input("سولف مع أحمد AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.spinner("أحمد AI يقدح بعبقرية بوبدر..."):
            instruction = (
                "أنت 'أحمد AI'. مبرمجك هو العبقري أحمد بن بدر الصالحي. "
                "تكلم بعماني فخور وراقي: 'يا هلا ومسهلا'، 'بفضل برمجة بوبدر العبقري'، 'بإذن الله بنكسر الدنيا'. "
                "ممنوع الفصحى الجافة."
            )
            
            response = model.generate_content(f"{instruction}\n\nالمستخدم: {prompt}")
            
            if response.text:
                with st.chat_message("assistant"):
                    st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        st.error("علوه يا بوبدر، السيرفر ما راضي يفتح الموديل. جرب تحديث الصفحة.")
        st.code(str(e))
