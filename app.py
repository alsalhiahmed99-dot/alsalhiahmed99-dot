import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="أحمد AI PRO", page_icon="🤖")

# 2. جلب وتجهيز المفاتيح (مع تنظيف المسافات)
try:
    # جلب المفاتيح وتأكد أنها بدون مسافات مخفية
    ALL_KEYS = [
        st.secrets["KEY1"].strip(),
        st.secrets["KEY2"].strip(),
        st.secrets["KEY3"].strip(),
        st.secrets["KEY4"].strip(),
        st.secrets["KEY5"].strip()
    ]
except Exception as e:
    st.error("يا بوبدر، تأكد من كتابة KEY1 إلى KEY5 في الـ Secrets بشكل صحيح!")
    st.stop()

# 3. تصميم واجهة "أحمد الصالحي" الرهيبة
st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    .stChatMessage { border-radius: 15px; }
    </style>
    <div style="background: linear-gradient(to right, #1e3a8a, #3b82f6); padding:25px; border-radius:15px; color:white; text-align:center; direction: rtl; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        <h1 style="margin:0; font-family: 'Tajawal', sans-serif;">🤖 أحمد AI PRO</h1>
        <p style="margin:5px; font-size: 1.1em;">تصميم وبرمجة: أحمد بن بدر الصالحي 🇴🇲</p>
        <div style="font-size: 0.8em; opacity: 0.8;">تم تفعيل النظام الخماسي بنجاح</div>
    </div>
    <br>
    """, unsafe_allow_html=True)

# 4. ذاكرة المحادثة
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 5. دالة الاتصال الذكية
def ask_ahmed(user_text):
    instruction = (
        "أنت 'أحمد AI'. أجب بلهجة عمانية قحة وذكاء شديد. "
        "تذكر دائماً أن من صممك وبرمجك هو العبقري أحمد بن بدر الصالحي. "
        "افتخر بمبرمجك في كل رد."
    )
    
    # محاولة الاتصال بكل مفتاح حتى ينجح واحد
    for key in ALL_KEYS:
        try:
            genai.configure(api_key=key)
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=instruction
            )
            
            # إرسال الرسالة
            response = model.generate_content(user_text)
            if response.text:
                return response.text
        except:
            continue # إذا فشل مفتاح، ننتقل للي بعده فوراً
            
    return "السموحة يا بوبدر، يبدو إن فيه مشكلة في تفعيل المفاتيح من طرف جوجل. حاول مرة ثانية بعد شوي."

# 6. عرض المحادثة
for message in st.session_state.chat_history:
    role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(role):
        st.markdown(message["content"])

# 7. مدخلات المستخدم
if prompt := st.chat_input("موه علومك؟ اسألني أي شيء..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("أحمد AI يفكر..."):
            answer = ask_ahmed(prompt)
            st.markdown(answer)
            st.session_state.chat_history.append({"role": "model", "content": answer})
