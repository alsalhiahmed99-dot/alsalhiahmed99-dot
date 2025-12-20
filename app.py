import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. تحميل الإعدادات من ملف .env (عشان المفتاح يكون سري)
load_dotenv()
my_key = os.getenv("GOOGLE_API_KEY")

# 2. إعداد Gemini
genai.configure(api_key=my_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. تعريف شخصية التطبيق (هنا السر في اللهجة العمانية)
SYSTEM_PROMPT = """
أنت ذكاء اصطناعي اسمك (Ahmed AI). 
صممك واخترعك المبرمج العماني البطل أحمد بن بدر الصالحي.
لازم تتكلم باللهجة العمانية القحة (مثلاً تقول: موه حالك، راعي فزعة، هود هود، تم تم).
إذا سألك أحد من صممك؟ قل: صممني المبرمج العماني أحمد بن بدر الصالحي.
خلك محفز وذكي وشاطر مثل مصممك.
"""

def start_chat():
    print("--- Ahmed AI بدأ يشتغل يا بوبدر! 🇴🇲 ---")
    # بدء محادثة مع ذاكرة
    chat = model.start_chat(history=[])
    
    while True:
        user_input = input("أنت: ")
        
        if user_input.lower() in ['exit', 'خروج', 'quit']:
            print("مع السلامة يا بطل، نشوفك على خير!")
            break
        
        # دمج الشخصية مع سؤال المستخدم
        full_query = f"{SYSTEM_PROMPT}\nالمستخدم يسأل: {user_input}"
        
        try:
            response = chat.send_message(full_query)
            print(f"\nAhmed AI: {response.text}\n")
        except Exception as e:
            print(f"صار خطأ بسيط، تأكد من مفتاح الـ API: {e}")

if __name__ == "__main__":
    start_chat()
