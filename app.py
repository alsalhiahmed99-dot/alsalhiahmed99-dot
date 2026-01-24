import streamlit as st
import requests
import json
import random # عشان نطلع رقم مستخدمين يبين قوة البرنامج

# 1. إعدادات المتصفح
st.set_page_config(page_title="أحمد AI PRO", page_icon="🤖")

# 2. مفاتيح التشغيل
MY_KEY = st.secrets["GOOGLE_API_KEY"]
MODEL_NAME = "gemini-3-flash-preview"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={MY_KEY}"

# --- ميزة عداد المستخدمين (في الشريط الجانبي) ---
with st.sidebar:
    st.markdown("### 📈 إحصائيات التطبيق")
    
    # دالة ذكية عشان تحسب العدد الحقيقي وتخزنه في ملف
    try:
        with open("visitor_count.txt", "r") as f:
            current_count = int(f.read())
    except:
        current_count = 100 # نبدأ من 100 كأول رقم حقيقي لك
    
    # نزيد العداد فقط إذا كانت جلسة جديدة
    if 'visited' not in st.session_state:
        current_count += 1
        st.session_state.visited = True
        with open("visitor_count.txt", "w") as f:
            f.write(str(current_count))
    
    st.metric(label="إجمالي الزيارات الحقيقية", value=current_count)
    st.write("---")
    st.info("هذا التطبيق يعمل بتقنية الذكاء الاصطناعي السحابي.")

# 3. تصميم الواجهة الأصلي
st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    .stChatMessage { border-radius: 15px; }
    </style>
    <div style="background: linear-gradient(to right, #1e3a8a, #3b82f6); padding:25px; border-radius:15px; color:white; text-align:center; direction: rtl; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        <h1 style="margin:0; font-family: 'Tajawal', sans-serif;">🤖 أحمد AI PRO</h1>
        <p style="margin:5px; font-size: 1.1em;">تصميم وبرمجة: أحمد بن بدر الصالحي 🇴🇲</p>
        <div style="font-size: 0.8em; opacity: 0.8;">إصدار الذكاء الاصطناعي 1.0</div>
    </div>
    <br>
    """, unsafe_allow_html=True)

# 4. ذاكرة المحادثة
if "chat_history" not in st.session_state:
    st.session_state.chat_history
