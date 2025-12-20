import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. تحميل المفتاح السري من ملف .env
load_dotenv()
my_key = os.getenv("GOOGLE_API_KEY")

# 2. إعداد الذكاء الاصطناعي
genai.configure(api_key=my_key)

# 3. اختيار الموديل (Gemini)
model = genai.GenerativeModel('gemini-1.5-flash')

def start_ahmed_ai():
    print("--- AHMED-AI جاهز للعمل يا بطل ---")
    while True:
        user_input = input("أحمد (أنت): ")
        if user_input.lower() in ['exit', 'خروج', 'quit']:
            break
        
        # إرسال السؤال للذكاء الاصطناعي
        response = model.generate_content(user_input)
        
        print(f"\nAhmed AI: {response.text}\n")

if __name__ == "__main__":
    start_ahmed_ai()
