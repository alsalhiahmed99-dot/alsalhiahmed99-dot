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

# 3. تصميم الواجهة الاحترافي (نفس ستايلك)
st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    .stChatMessage { border-radius: 15px; }
    </style>
    <div style="background: linear-gradient(to right, #1e3a8a, #3b82f6); padding:25px; border-radius:15px; color:white; text-align:center; direction: rtl; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        <h1 style="margin:0; font-family: 'Tajawal', sans-serif;">🤖 أحمد AI PRO</h1>
        <p style="margin:5px; font-size: 1.1em;">تصميم وبرمجة: أحمد بن بدر الصالحي 🇴🇲</p>
        <div style="font-size: 0.8em; opacity: 0.8;">إصدار 2026 الصاروخي (النسخة المنضبطة)</div>
    </div>
    <br>
    """, unsafe_allow_html=True)

# 4. ذاكرة المحادثة
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 5. دالة التواصل مع الذكاء الاصطناعي (تم تحسينها لمنع التخريف)
def ask_ahmed(text):
    is_first_reply = len(st.session_state.chat_history) == 0
    
    if is_first_reply:
        extra_instruction = "في أول رد، سلم بلهجة عمانية هادئة ووقورة، واذكر إنك من برمجة أحمد الصالحي باختصار."
    else:
        extra_instruction = "جاوب على قد السؤال بأسلوب رزين ومحترم."

    # تعليمات صارمة لضبط الأسلوب ومنع الردود الغريبة
    system_instruction = (
        f"أنت ذكاء اصطنا
