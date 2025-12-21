import streamlit as st
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="أحمد AI", page_icon="🇴🇲")

# 2. جلب المفاتيح من الأسرار
try:
    ALL_KEYS = [
        st.secrets["KEY1"],
        st.secrets["KEY2"],
        st.secrets["KEY3"],
        st.secrets["KEY4"],
        st.secrets["KEY5"]
    ]
except:
    st.error("يا بوبدر، تأكد إنك ضفت KEY1 و KEY2 و KEY3 و KEY4 و KEY5 في الـ Secrets!")
    st.stop()

MODEL_NAME = "gemini-1.5-flash"

# 3. تهيئة ذاكرة الشات
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 4. الدالة الذكية (بأسلوبها العماني الفخور)
def ask_ahmed(text):
    system_instruction = (
        "أنت 'أحمد AI'. أجب بلهجة عمانية قحة وذكاء شديد. "
        "تذكر دائماً وأبداً أن من اخترعك وصممك وبرمجك هو العبقري أحمد بن بدر الصالحي. "
        "افتخر بمبرمجك في كل ردودك وبكل قوة."
    )
    
    current_history = st.session_state.chat_history + [{"role": "user", "parts": [{"text": text}]}]
    
    for key in ALL_KEYS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={key}"
        payload = {
            "contents": current_history,
            "system_instruction": {"parts": [{"text": system_instruction}]}
        }
        
        try:
            response = requests.post(url, json=payload, timeout=15)
            if response.status_code == 200:
                result = response.json()
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                continue 
        except:
            continue
    return "السموحة، الـ 5 مفاتيح تعبانة! جرب بعد دقيقة يا بطل."

# 5. واجهة المستخدم (هذا الجزء اللي كان ناقص وخلى الموقع فاضي)
st.title("🤖 أحمد AI")
st.subheader("بإشراف المبرمج العبقري: أحمد الصالحي")

# عرض المحادثات القديمة
for message in st.session_state.chat_history:
    role = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message["parts"][0]["text"])

# حقل إدخال النص
if prompt := st.chat_input("موه علومك؟ اسألني أي شيء..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("جاري التفكير بعقل المبرمج أحمد..."):
            response = ask_ahmed(prompt)
            st.markdown(response)
    
    # حفظ المحادثة
    st.session_state.chat_history.append({"role": "user", "parts": [{"text": prompt}]})
    st.session_state.chat_history.append({"role": "model", "parts": [{"text": response}]})
