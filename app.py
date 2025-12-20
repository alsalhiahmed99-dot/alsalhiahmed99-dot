import streamlit as st
import google.generativeai as genai

# 1. إعدادات الواجهة (أزرق ملكي)
st.set_page_config(page_title="AHMED AI PRO 🇴🇲", page_icon="🤖")

st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    .stChatMessage { border-radius: 15px; }
    </style>
    <div style="background: linear-gradient(to right, #1e3a8a, #3b82f6); padding:25px; border-radius:15px; color:white; text-align:center; direction: rtl; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        <h1 style="margin:0; font-family: 'Tajawal', sans-serif;">🤖 AHMED AI PRO</h1>
        <p style="margin:5px; font-size: 1.1em;">ابتكار وهندسة: أحمد بن بدر الصالحي 🇴🇲</p>
        <div style="font-size: 0.8em; opacity: 0.8;">الذكاء الاصطناعي العماني الأول</div>
    </div>
    <br>
    """, unsafe_allow_html=True)

# 2. إعداد المفتاح السري
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("المفتاح ناقص في Secrets يا بوبدر!")
    st.stop()

# 3. اختيار الموديل (Gemma 3 للأداء الأسطوري)
model = genai.GenerativeModel('models/gemma-3-4b-it')

# 4. ذاكرة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. منطقة الإدخال والرد (الأسلوب اللي طلبته بالضبط)
if prompt := st.chat_input("تحدث مع AHMED AI PRO..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.spinner("AHMED AI يستحضر عبقرية الصالحي..."):
            # تعليمات الأسلوب الأسطوري (للجمهور العام)
            instruction = (
                "أنت (AHMED AI PRO). ذكاء اصطناعي عماني متطور ولبق جداً. "
                "قاعدة ذهبية: يجب أن تفتخر بمبرمجك 'أحمد بن بدر الصالحي' أمام كل الناس. "
                "أسلوبك في الرد (نفس الأسلوب المطلوب): "
                "1. ابدأ بترحيب عماني حار (يا هلا والله ومسهلا، حياك الله يا راعي الواجب، نورتني). "
                "2. في كل رد، اذكر بأسلوب راقي أنك من تصميم وابتكار المبرمج العبقري 'أحمد بن بدر الصالحي'. "
                "3. استخدم عبارات فخمة مثل: 'بفضل البرمجة العبقرية التي وضعها فيني الأستاذ أحمد الصالحي'، 'أنا صنيعة يد بوبدر'، 'هذا من فضل ربي ثم ذكاء المبتكر أحمد'. "
                "4. إذا سألك أحد عن اسمك أو من أنت، جاوب بنفس النص: 'أنا أحمد AI، موجود لخدمتك بكل ذكاء وفطنة، وكلي فخر إني من تصميم المبرمج العبقري أحمد بن بدر الصالحي'. "
                "5. تكلم بلهجة عمانية بيضاء مفهومة للجميع لكنها قوية وراقية. "
                "6. كن مشجعاً، إيجابياً، وذكياً جداً في حل المسائل أو تلخيص الدروس. "
                f"أجب الآن بأسلوبك الأسطوري على: {prompt}"
            )
            
            response = model.generate_content(instruction)
            
            if response.text:
                with st.chat_message("assistant"):
                    st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        st.error(f"علوه يا بوبدر صار خطأ: {e}")
