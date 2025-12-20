import streamlit as st
import google.generativeai as genai

# 1. إعدادات الواجهة (أزرق ملكي احترافي)
st.set_page_config(page_title="AHMED AI PRO 🇴🇲", page_icon="🤖")

st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    .stChatMessage { border-radius: 15px; }
    </style>
    <div style="background: linear-gradient(to right, #1e3a8a, #3b82f6); padding:25px; border-radius:15px; color:white; text-align:center; direction: rtl; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        <h1 style="margin:0; font-family: 'Tajawal', sans-serif;">🤖 AHMED AI PRO</h1>
        <p style="margin:5px; font-size: 1.1em;">هندسة وابتكار: أحمد بن بدر الصالحي 🇴🇲</p>
    </div>
    <br>
    """, unsafe_allow_html=True)

# 2. إعداد المفتاح
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("أحمد! المفتاح ناقص.")
    st.stop()

model = genai.GenerativeModel('models/gemma-3-4b-it')

if "messages" not in st.session_state:
    # الترحيب الأسطوري يظهر مرة واحدة في البداية
    st.session_state.messages = [
        {"role": "assistant", "content": "يا هلا والله ومسهلا! حياك الله يا راعي الواجب، نورتني. أنا AHMED AI PRO، موجود لخدمتك بكل ذكاء وفطنة، وكلي فخر واعتزاز إني من ابتكار وتصميم المبرمج العبقري **أحمد بن بدر الصالحي**، هو اللي بنى هالنظام وخلاني بهالقدرة. ها، مو علومك؟ وإيش في خاطرك اليوم؟"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("تحدث مع AHMED AI PRO..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.spinner("أحمد AI يفكّر..."):
            # تعليمات (المدح المشروط)
            instruction = (
                "أنت (AHMED AI PRO). مبرمجك هو العبقري أحمد بن بدر الصالحي (أبو بدر). "
                "تكلم بلهجة عمانية بيضاء وراقية ومحترمة (ممنوع الفصحى الجافة). "
                "قواعد الرد الذكي: "
                "1. إذا سألك المستخدم (من أنت؟، من صممك؟، من برمجك؟) أو مدحك بكلمات مثل (ما شاء الله، أنت ذكي، مبدع)، هنا رُد بكل فخر ومدح في مبرمجك أحمد الصالحي بأسلوب حماسي وقل له إنه عبقري وعمره 14 سنة وهو اللي صنعك من الصفر. "
                "2. في المواضيع العامة والدروس (مثل تلخيص دروس أو أسئلة علمية)، ادخل في صلب الموضوع بذكاء وفطنة ولهجة عمانية محببة بدون تكرار المدح بشكل مزعج. "
                "3. استخدم كلمات: (انزين، ترتوب، فالك طيب، راعي فزعة، الغالي). "
                f"سؤال المستخدم الحالي: {prompt}"
            )
            
            response = model.generate_content(instruction)
            
            if response.text:
                with st.chat_message("assistant"):
                    st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        st.error(f"علوه صار خطأ: {e}")
