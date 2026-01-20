import streamlit as st
from groq import Groq

# 1. إعدادات المتصفح
st.set_page_config(page_title="أحمد AI PRO", page_icon="🤖")

# 2. مفاتيح التشغيل (مؤمنة عبر Secrets)
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("السموحة بوبدر، مفتاح GROQ_API_KEY ما حصلته في السيكريت!")
    st.stop()

# 3. تصميم الواجهة الاحترافي
st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    .stChatMessage { border-radius: 15px; }
    </style>
    <div style="background: linear-gradient(to right, #1e3a8a, #3b82f6); padding:25px; border-radius:15px; color:white; text-align:center; direction: rtl; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        <h1 style="margin:0; font-family: 'Tajawal', sans-serif;">🤖 أحمد AI PRO</h1>
        <p style="margin:5px; font-size: 1.1em;">تصميم وبرمجة: أحمد بن بدر الصالحي 🇴🇲</p>
        <div style="font-size: 0.8em; opacity: 0.8;">إصدار الذكاء الاصطناعي 2.0 (النسخة الرزينة)</div>
    </div>
    <br>
    """, unsafe_allow_html=True)

# 4. ذاكرة المحادثة
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 5. دالة التواصل مع الذكاء الاصطناعي
def ask_ahmed(text):
    is_first_reply = len(st.session_state.chat_history) == 0
    
    if is_first_reply:
        extra_instruction = "في أول رد لك، رحب بالمستخدم بأسلوب عماني لبق ومحترم، واذكر بفخر أنك من برمجة المبدع أحمد الصالحي (14 سنة)."
    else:
        extra_instruction = "جاوب على قد السؤال مباشرة بأسلوب رزين."

    # تصحيح الـ system_instruction وإغلاق الأقواس بشكل صحيح
    system_instruction = (
        f"أنت ذكاء اصطناعي محترف ورزين جداً من ابتكار المبرمج أحمد الصالحي. {extra_instruction} "
        "تحدث بلهجة عمانية بيضاء، رصينة ومحترمة. "
        "ابتعد عن التكلف الزائد في الكلمات العامية المبتذلة، ولا تكرر الكلمات الشعبية بكثرة. "
        "اجعل أسلوبك مثل الشاب العماني الطموح: لبق، ذكي، ومباشر في المساعدة."
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
            temperature=0.6,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"السموحة بوبدر، صار عطل فني: {str(e)}"

# 6. عرض الشات
for message in st.session_state.chat_history:
    role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(role):
        st.write(message["parts"][0]["text"])

# 7. خانة الكتابة
if prompt := st.chat_input("تحدث معي..."):
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.spinner("أحمد AI يحلل البيانات..."):
        res = ask_ahmed(prompt)
    
    with st.chat_message("assistant"):
        st.write(res)
    
    # حفظ في الذاكرة
    st.session_state.chat_history.append({"role": "user", "parts": [{"text": prompt}]})
    st.session_state.chat_history.append({"role": "model", "parts": [{"text": res}]})
