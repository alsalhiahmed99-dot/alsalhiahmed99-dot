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

# 3. تصميم الواجهة (ستايل مبرمجنا أحمد الصالحي)
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

# 5. الدالة الصارمة لضبط السنع والعماني القح
def ask_ahmed(text):
    # هنا "تأديب" الموديل عشان يتكلم عماني وما يلف ويدور
    system_instruction = (
        "أنت ذكاء اصطناعي عماني رزين وقح، مبرمجك هو أحمد الصالحي. "
        "ممنوع منعاً باتاً تتكلم فصحى أو تقول 'أنا مبرمج للفصحى' أو 'أنا برنامج'. "
        "تكلم عماني قح ورزين مثل رجال المجالس. "
        "ردودك تكون واثقة، وإذا حد سألك عن السنع، قوله: 'أنا مسنع ومتربي على إيد أحمد الصالحي'. "
        "استخدم كلمات: (هيش، تو، باغي، غايته، علامك، حبابي، نوبه، كذاك). "
        "خلك ذيب، رزين، ومباشر."
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
            temperature=0.8, # رفعناه شوي عشان يكون الكلام طبيعي وغير جامد
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"السموحة، السيرفر تعبان شوي."

# 6. العرض
for message in st.session_state.chat_history:
    role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(role):
        st.write(message["parts"][0]["text"])

# 7. الإدخال
if prompt := st.chat_input("تكلم مع أحمد AI..."):
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.spinner("لحظة، أحمد AI يضبط الرد..."):
        res = ask_ahmed(prompt)
    
    with st.chat_message("assistant"):
        st.write(res)
    
    st.session_state.chat_history.append({"role": "user", "parts": [{"text": prompt}]})
    st.session_state.chat_history.append({"role": "model", "parts": [{"text": res}]})
