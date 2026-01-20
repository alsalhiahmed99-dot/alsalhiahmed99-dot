import streamlit as st
from groq import Groq

# 1. إعدادات المتصفح
st.set_page_config(page_title="أحمد AI PRO", page_icon="🤖")

# 2. مفاتيح التشغيل (مؤمنة عبر Secrets في Streamlit Cloud)
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("السموحة بوبدر، مفتاح GROQ_API_KEY ما حصلته في السيكريت! تأكد من إضافته.")
    st.stop()

# 3. تصميم الواجهة الاحترافي (نفس الستايل اللي تحبه)
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

# 4. ذاكرة المحادثة (نظام chat_history)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 5. دالة التواصل مع Groq (بأسلوب عماني رزين ومثقف)
def ask_ahmed(text):
    is_first_reply = len(st.session_state.chat_history) == 0
    
    if is_first_reply:
        extra_instruction = "في أول رد لك، رحب بالمستخدم بأسلوب عماني لبق ومحترم، واذكر بفخر أنك من برمجة المبدع أحمد الصالحي (14 سنة)."
    else:
        extra_instruction = "جاوب على قد السؤال مباشرة بأسلوب رزين ولا تكرر الكلام عن مبرمجك إلا للضرورة."

    # تعديل "رأس" الذكاء الاصطناعي لضبط الأسلوب
    system_instruction = (
        f"أنت ذكاء اصطناعي محترف ورزين جداً من ابتكار المبرمج أحمد الصالحي. {extra_instruction} "
        "تحدث بلهجة عمانية بيضاء، رصينة ومحترمة (لهجة المثقفين). "
