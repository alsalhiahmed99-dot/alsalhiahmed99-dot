import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(page_title="Ahmad AI PRO", page_icon="🤖", layout="centered")

# 2. API Keys and URL
MY_KEY = st.secrets["GOOGLE_API_KEY"]
MODEL_NAME = "gemini-1.5-flash"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={MY_KEY}"

# 3. Custom CSS and UI
st.markdown("""
    <style>
    .main { background-color: #0b1117; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    img { border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.5); }
    </style>
    <div style="background: linear-gradient(to right, #1e3a8a, #3b82f6); padding:20px; border-radius:15px; color:white; text-align:center; direction: rtl;">
        <h1 style="margin:0;">🤖 أحمد AI PRO</h1>
        <p style="margin:5px;">تصميم وبرمجة المبدع: أحمد بن بدر الصالحي 🇴🇲</p>
    </div>
    <br>
    """, unsafe_allow_html=True)

# 4. Chat History Initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 5. Image Generation Function
def generate_image(prompt):
    clean_prompt = prompt.replace(" ", "%20")
    return f"https://pollinations.ai/p/{clean_prompt}?width=1024&height=1024&seed=42&model=flux"

# 6. AI Communication Function
def ask_ahmed(text):
    system_instruction = "You are Ahmad AI. Invented by Ahmad bin Badr Al Salhi, 14 years old. Answer in Omani dialect."
    contents = []
    for msg in st.session_state.chat_history:
        contents.append({"role": msg["role"], "parts": [{"text": msg["parts"][0]["text"]}]})
    contents.append({"role": "user", "parts": [{"text": text}]})
    
    payload = {
        "contents": contents,
        "system_instruction": {"parts": [{"text": system_instruction}]}
    }
    
    try:
        response = requests.post(URL, json=payload, timeout=15)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return "السموحة بوبدر، جوجل عنده ضغط. حاول مرة ثانية!"
    except:
        return "مشكلة في الشبكة، شيك على الواي فاي!"

# 7. Display Chat History
for message in st.session_state.chat_history:
    role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(role):
        st.write(message["parts"][0]["text"])

# 8. Chat Input Area
prompt = st.chat_input("سولف معي أو اطلب رسمة...")

if prompt:
    with st.chat_message("user"):
        st.write(prompt)
    
    # Check for image request
    image_keywords = ["ارسم", "رسم", "صورة", "صوره", "draw"]
    if any(word in prompt.lower() for word in image_keywords):
        with st.spinner("جاري الإبداع..."):
            img_url = generate_image(prompt)
            with st.chat_message("assistant"):
                st.image(img_url)
            st.session_state.chat_history.append({"role": "user", "parts": [{"text": prompt}]})
            st.session_state.chat_history.append({"role": "model", "parts": [{"text": "Image Generated Successfully"}]})
    else:
        with st.spinner("يفكر..."):
            res = ask_ahmed(prompt)
            with st.chat_message("assistant"):
                st.write(res)
            st.session_state.chat_history.append({"role": "user", "parts": [{"text": prompt}]})
            st.session_state.chat_history.append({"role": "model", "parts": [{"text": res}]})
    
    st.rerun()
