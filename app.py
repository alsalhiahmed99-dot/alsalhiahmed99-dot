import streamlit as st
import google.generativeai as genai

# 1. إعدادات الواجهة (خلفية بيضاء وتنسيق نظيف)
st.set_page_config(page_title="AHMED AI PRO 🇴🇲", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    /* جعل الخلفية بيضاء بالكامل */
    .stApp {
        background-color: #ffffff;
    }
    
    /* تنسيق فقاعات الدردشة */
    .stChatMessage {
        padding: 1rem;
        border-radius: 20px;
        margin-bottom: 12px;
        max-width: 85%;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* كلام المستخدم (أنت) - يمين وبلون أزرق فاتح */
    div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        margin-left: auto;
        background-color: #e3f2fd !important; /* أزرق سماوي خفيف */
        color: #0d47a1;
        direction: rtl;
        border: 1px solid #bbdefb;
    }

    /* كلام البوت (أحمد AI) - يسار وبلون رمادي فاتح */
    div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        margin-right: auto;
        background-color: #f5f5f5 !important; /* رمادي خفيف جداً */
        color: #333333;
        direction: rtl;
        border: 1px solid #eeeeee;
    }

    /* إخفاء الأيقونات والأسماء تماماً لشكل أنظف */
    [data-testid="chatAvatarIcon-user"], [data-testid="chatAvatarIcon-assistant"] { display: none; }
    .st-emotion-cache-10o0f9z { display: none; } 
    
    /* رأس الصفحة (Header) */
    .header-box {
        background: linear-gradient(to right, #1e3a8a, #3b82f6);
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        direction: rtl;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    </style>
    
    <div class="header-box">
        <h1 style="margin:0; font-family: 'Tajawal', sans-serif;">🤖 AHMED AI PRO</h1>
        <p style="margin:5px; font-size: 1.1em;">هندسة وابتكار العبقري: أحمد بن بدر الصالحي 🇴🇲</p>
    </div>
    <br
