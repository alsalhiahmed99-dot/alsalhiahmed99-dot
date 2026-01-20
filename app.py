import streamlit as st
from groq import Groq

# 1. إعدادات المتصفح
st.set_page_config(page_title="أحمد AI PRO", page_icon="🤖")

# 2. مفاتيح التشغيل
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("السموحة بوبدر، مفتاح GROQ_API_KEY ما موجود!")
    st.stop()

# 3. تصميم الواجهة
st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    .stChatMessage { border-radius: 15px; }
    </style>
    <div style="background: linear-gradient(to right, #1e3a8a, #3b82f6); padding:25px; border-radius:15px; color:white; text-align:center; direction: rtl;">
        <h1 style="margin:0;">🤖 أحمد AI PRO</h1>
        <p style="margin:5px;">تصميم وبرمجة: أحمد الصالحي 🇴🇲</p>
    </div>
    <br>
    """, unsafe_allow_html=True)

# 4. الذاكرة
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 5. الدالة الصارمة لضبط اللهجة
def ask_ahmed(text):
    # تعليمات "الخيزران" عشان يتأدب الموديل
    system_instruction = (
        "أنت ذكاء اصطناعي رزين، مبرمجك هو أحمد الصالحي. "
        "ممنوع تتكلم فصحى. ممنوع تقول 'أنا سعيد' أو 'في ماذا يمكنني مساعدتك'. "
        "تكلم عماني رزين (كلام رجال). "
        "أمثلة للردود:\n"
        "المستخدم: هلا -> الرد: يا هلا بيك، مرحبتين. تفضل الغالي، ويش في خاطرك؟\n"
        "المستخدم: وش الأخبار -> الرد: الأمور طيبة الحمدلله، من صوبك؟ وكيف أقدر أخدمك؟\n"
        "المستخدم: من برمجك -> الرد: أنا من برمجة أحمد الصالحي، والبركة فيه.\n"
        "التزم بهذا الأسلوب المختصر والرزين."
    )
    
    messages = [{"role": "system", "content": system_instruction}]
    for msg in st.session_state.chat_history:
        role = "assistant" if msg["role"] == "model" else "user"
        messages.append({"role": role, "content": msg["parts"][0]["text"]})
    
    messages.append({"role": "user", "content": text})

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.4, # قللنا الرقم عشان يكون الرد ثابت ورزين
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"السموحة، صار خطأ: {str(e)}"

# 6. العرض
for message in st.session_state.chat_history:
    role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(role):
        st.write(message["parts"][0]["text"])

# 7. الإدخال
if prompt := st.chat_input("تحدث معي..."):
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.spinner("لحظة..."):
        res = ask_ahmed(prompt)
    
    with st.chat_message("assistant"):
        st.write(res)
    
    st.session_state.chat_history.append({"role": "user", "parts": [{"text": prompt}]})
    st.session_state.chat_history.append({"role": "model", "parts": [{"text": res}]})
