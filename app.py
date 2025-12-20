import streamlit as st
import google.generativeai as genai

# 1. إعدادات الواجهة والهوية البصرية
st.set_page_config(page_title="AHMED AI PRO 🇴🇲", page_icon="🤖", layout="centered")

# تصميم CSS احترافي لترتيب الفقاعات (يمين ويسار) وإخفاء الأيقونات والأسماء
st.markdown("""
    <style>
    /* تغيير خلفية التطبيق */
    .stApp { background-color: #0b0e14; }
    
    /* تنسيق فقاعات الدردشة */
    .stChatMessage {
        padding: 1rem;
        border-radius: 15px;
        margin-bottom: 10px;
        max-width: 80%;
    }
    
    /* كلام المستخدم (أنت) يروح يمين */
    [data-testid="chatAvatarIcon-user"] { display: none; }
    div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        margin-left: auto;
        background-color: #1e3a8a !important; /* أزرق غامق */
        color: white;
        direction: rtl;
    }

    /* كلام البوت (أحمد AI) يروح يسار */
    [data-testid="chatAvatarIcon-assistant"] { display: none; }
    div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        margin-right: auto;
        background-color: #262730 !important; /* رمادي غامق */
        color: white;
        direction: rtl;
    }

    /* إخفاء اسم المساعد والمستخدم */
    .st-emotion-cache-10o0f9z { display: none; } 
    
    /* رأس الصفحة الفخم */
    .header-box {
        background: linear-gradient(to right, #1e3a8a, #3b82f6);
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        direction: rtl;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    </style>
    
    <div class="header-box">
        <h1 style="margin:0; font-family: 'Tajawal', sans-serif;">🤖 AHMED AI PRO</h1>
        <p style="margin:5px; font-size: 1.1em;">هندسة وابتكار العبقري: أحمد بن بدر الصالحي 🇴🇲</p>
    </div>
    <br>
    """, unsafe_allow_html=True)

# 2. إعداد المفتاح
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("المفتاح ناقص في الإعدادات!")
    st.stop()

# اختيار الموديل (تأكد من استخدام الموديل الشغال عندك)
model = genai.GenerativeModel('models/gemma-3-4b-it')

# 3. الترحيب الأسطوري (موجه للجمهور العام)
if "messages" not in st.session_state:
    welcome_msg = (
        "يا هلا والله ومسهلا بك يا ضيفنا العزيز! نورت شاشة **AHMED AI PRO** 🌟\n\n"
        "أنا مساعدك الذكي، من ابتكار وهندسة المبرمج العماني النابغة **أحمد بن بدر الصالحي** (عمره 14 سنة). "
        "بوبدر صممني بذكاء وفطنة عشان أخدمك وأرفع راس العمانيين في عالم التكنولوجيا.\n\n"
        "آمرني الغالي، ويش في خاطرك اليوم؟ أنا جاهز لكل تساؤلاتك بلمسة عمانية أصيلة!"
    )
    st.session_state.messages = [{"role": "assistant", "content": welcome_msg}]

# عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. استقبال كلام المستخدم ومعالجته
if prompt := st.chat_input("سولف مع AHMED AI PRO..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.spinner("أحمد AI يقدح بذكاء..."):
            # تعليمات موجهة للجمهور العام (نشر)
            instruction = (
                "أنت (AHMED AI PRO). مبرمجك ومخترعك هو العبقري العماني أحمد بن بدر الصالحي. "
                "خاطب المستخدم بلهجة عمانية بيضاء (للجمهور العام): "
                "1. كن محترماً، فخوراً، وذكياً جداً. "
                "2. استخدم كلمات مثل: (فالك طيب، نورتنا، الغالي، ذخر، ما يهمك). "
                "3. في كل مرة يمدحك المستخدم أو يسألك من أنت، أخبره أنك فخر الصناعة العمانية بيد أحمد الصالحي. "
                "4. إذا سألك المستخدم 'من أنت'، قل له: أنا أحمد AI، صنيعة عقل المبرمج بوبدر الصالحي. "
                f"أجب بأسلوب عماني فخم على: {prompt}"
            )
            
            response = model.generate_content(instruction)
            
            if response.text:
                with st.chat_message("assistant"):
                    st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        st.error(f"علوه يا بوبدر، السيرفر فيه شي: {e}")
