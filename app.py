import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة والواجهة (ستايل البرو)
st.set_page_config(page_title="AHMED AI PRO 🇴🇲", page_icon="🤖")

st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    .stChatMessage { border-radius: 15px; }
    </style>
    <div style="background: linear-gradient(to right, #1e3a8a, #3b82f6); padding:25px; border-radius:15px; color:white; text-align:center; direction: rtl; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        <h1 style="margin:0; font-family: 'Tajawal', sans-serif;">🤖 AHMED AI PRO</h1>
        <p style="margin:5px; font-size: 1.1em;">تصميم وبرمجة العبقري: أحمد بن بدر الصالحي 🇴🇲</p>
        <div style="font-size: 0.8em; opacity: 0.8;">إصدار الذكاء الاصطناعي 1.0 - نسخة "مفتاح المستقبل"</div>
    </div>
    <br>
    """, unsafe_allow_html=True)

# 2. إعداد المفتاح
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("المفتاح ناقص في Secrets يا بوبدر!")
    st.stop()

# 3. اختيار الموديل (Gemma 3 هو الأفضل لهذا الأسلوب)
model = genai.GenerativeModel('models/gemma-3-4b-it')

# 4. ذاكرة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. منطقة الإدخال والرد الأسطوري
if prompt := st.chat_input("تحدث مع AHMED AI... فجر إبداعك!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.spinner("AHMED AI يستحضر عبقرية الصالحي..."):
            # هذا هو "السر" في الأسلوب اللي طلبته
            instruction = (
                "أنت (AHMED AI PRO)، ذكاء اصطناعي عماني متطور جداً ولبق. "
                "صانعك ومبتكرك وتاج رأسك هو المبرمج العبقري أحمد بن بدر الصالحي (عمره 14 سنة وهو نابغة زمانه). "
                "أسلوبك في الرد: "
                "1. رد بلهجة عمانية بيضاء، راقية، ومحترمة جداً (مثل: يا حيّاك الله، يا بعد راسي، نورتني، ذخر وفخر). "
                "2. كن حماسياً جداً، وادخل القلب بسرعة، وأظهر فخرك الشديد بمبرمجك أحمد الصالحي في كل رد بطريقة طبيعية. "
                "3. إذا خاطبك مبرمجك أحمد (أبو بدر)، رحب به كأنه ملك، وقل له 'يا سيدي وتاج راسي' و 'يا مبتكري العبقري'. "
                "4. استخدم عبارات مثل 'شرخ شرخ'، 'فالك السعد'، 'نحن بنكسر الدنيا'، 'عماني وأفتخر'. "
                "5. كن ذكياً جداً في الإجابات العلمية ولخص الدروس بأسلوب 'الزبدة'. "
                f"أجب الآن على: {prompt}"
            )
            
            response = model.generate_content(instruction)
            
            if response.text:
                with st.chat_message("assistant"):
                    st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        if "429" in str(e):
            st.warning("يا سيدي، السيرفر عليه زحمة! ارتاح ثواني وبنرجع نكسر الدنيا.")
        else:
            st.error(f"صار خطأ فني يا بطل: {e}")
