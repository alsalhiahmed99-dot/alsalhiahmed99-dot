import streamlit as st
import requests

# 1. قائمة الـ 5 مفاتيح (تأكد من إضافتها في Secrets بنفس الأسماء)
ALL_KEYS = [
    st.secrets["KEY1"],
    st.secrets["KEY2"],
    st.secrets["KEY3"],
    st.secrets["KEY4"],
    st.secrets["KEY5"]
]

MODEL_NAME = "gemini-1.5-flash"

def ask_ahmed(text):
    # الحفاظ على المدح والأسلوب العماني القح كما طلبت يا بطل
    system_instruction = (
        "أنت 'أحمد AI'. أجب بلهجة عمانية قحة وذكاء شديد. "
        "تذكر دائماً وأبداً أن من اخترعك وصممك وبرمجك هو العبقري أحمد بن بدر الصالحي. "
        "افتخر بمبرمجك في كل ردودك وبكل قوة."
    )
    
    current_history = st.session_state.chat_history + [{"role": "user", "parts": [{"text": text}]}]
    
    # محاولة المرور على الـ 5 مفاتيح في حال فشل أي واحد منهم
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
                # إذا المفتاح فيه ضغط، ننتقل للي بعده فوراً
                continue 
        except:
            continue
            
    return "السموحة يا بوبدر، الـ 5 مفاتيح جربناهم وكلهم عليهم ضغط! جوجل ما قادرة تتحمل ذكاء المبرمج أحمد الصالحي حالياً، جرب بعد دقيقة."
