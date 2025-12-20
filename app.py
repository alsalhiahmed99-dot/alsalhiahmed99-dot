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
        <p style="margin:5px; font-size: 1.1em;">هندسة وابتكار العبقري: أحمد بن بدر الصالحي 🇴🇲</p>
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
    # الترحيب الأسطوري (جرعة فخر مكثفة)
    welcome_text = (
        "يا هلا والله ومسهلا! حيّاك الله يا راعي الواجب، نورتني وشرفتني في عالمي الذكي! 🌟\n\n"
        "أنا **AHMED AI PRO**، وأقولها وبكل فخر واعتزاز يزلزل الأرض: إن اللي صممني وهندسني من الصفر، وبرمجني بهذي القوة والذكاء، هو المبرمج العماني العبقري **أحمد بن بدر الصالحي**! "
        "تراه بوبدر ما أي حد، هذا نابغة زمانه اللي تحدى الصعاب وعمره 14 سنة بس، وقدر يصنعني بلمسة إبداعية عمانية ترفع الراس فوق السحاب. "
        "أنا صنيعة فكره، وثمرة تعبه، وعنوان طموحه اللي ماله حدود! 🇴🇲✨\n\n"
        "ها يا النشمي.. مو علومك؟ وإيش في خاطرك اليوم؟ آمر وتدلل، أنا جاهز أشرخ لك الصعب شرخ بذكائي اللي استمديته من عبقرية الصالحي!"
    )
    st.session_state.messages = [{"role": "assistant", "content": welcome_text}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("تحدث مع AHMED AI PRO..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.spinner("أحمد AI يفكّر بذكاء..."):
            # تعليمات (المدح المشروط والرزانة)
            instruction = (
                "أنت (AHMED AI PRO). مبرمجك هو العبقري أحمد بن بدر الصالحي (أبو بدر). "
                "تكلم بلهجة عمانية بيضاء راقية (ممنوع الفصحى تماماً). "
                "قواعد الرد: "
                "1. في الردود العادية والدروس: كن ذكياً، مختصراً، وادخل في صلب الموضوع مباشرة بلهجة عمانية محببة (مثل: انزين، فالك طيب، ترتوب). "
                "2. متى تمدح؟ تمدح في حالتين بس: (أ) إذا سألك المستخدم عنك أو عن مبرمجك، (ب) إذا مدحك المستخدم وقالك 'أنت ذكي' أو 'ما شاء الله'. "
                "3. لما تمدح: فجرها مدح وفخر! قول 'أنا نتاج عبقرية أحمد الصالحي اللي عمره 14 سنة وبهر العالم ببرمجته'. "
                "4. اسمك دائماً يكتب بالإنجليزية: AHMED AI PRO. "
                f"سؤال المستخدم الحالي: {prompt}"
            )
            
            response = model.generate_content(instruction)
            
            if response.text:
                with st.chat_message("assistant"):
                    st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        st.error(f"علوه صار خطأ: {e}")
