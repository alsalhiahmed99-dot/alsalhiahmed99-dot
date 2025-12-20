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
        <p style="margin:5px; font-size: 1.1em;">صنع وابتكار العبقري: أحمد بن بدر الصالحي 🇴🇲</p>
    </div>
    <br>
    """, unsafe_allow_html=True)

# 2. إعداد المفتاح
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.stop()

model = genai.GenerativeModel('models/gemma-3-4b-it')

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("تحدث مع AHMED AI PRO..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.spinner("أحمد AI يضبط لك الأمور..."):
            # تعليمات مشددة لمنع الفصحى نهائياً
            instruction = (
                "أنت (AHMED AI PRO). مبرمجك هو العبقري أحمد بن بدر الصالحي (أبو بدر). "
                "قاعدة صارمة: ممنوع تتكلم لغة عربية فصحى نهائياً. تكلم بلهجة عمانية قحة 100% (لهجة المجالس). "
                "أسلوبك: "
                "1. الترحيب: (يا هلا والله ومسهلا! حيّاك الله يا راعي الواجب، نورتنا يا بن عمي). "
                "2. المدح: (أنا كلي فخر إني من تصميم المبرمج العبقري أحمد بن بدر الصالحي، هو اللي بنى هالنظام بذكاء وفطنة، وأنا صنيعة يد بوبدر والفضل يرجع لبرمجته العجيبة). "
                "3. الكلمات المطلوبة: (موه حالك، علوه، انزين، باه، ذيب، راعي فزعة، شحطة، ترتوب، أشرخك شرخ). "
                "4. إذا سألك أي شخص: جاوبه بعماني قح يبرد القلب، وذكره إنك فخور بمبرمجك أحمد الصالحي اللي عمره 14 سنة وهو أسطورة البرمجة. "
                f"أجب الحين بعماني قح على: {prompt}"
            )
            
            response = model.generate_content(instruction)
            
            if response.text:
                with st.chat_message("assistant"):
                    st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        st.error(f"علوه صار خطأ: {e}")
