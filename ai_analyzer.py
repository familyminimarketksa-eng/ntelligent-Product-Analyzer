import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

async def analyze_reviews_with_ai(product_title: str, reviews: list):
    if not reviews:
        return {
            "verdict": "সন্দেহজনক / পর্যাপ্ত ডাটা নেই",
            "score": 0,
            "pros": ["রিভিউ খুঁজে পাওয়া যায়নি"],
            "cons": ["সেলার পেজে ডাইরেক্ট রিভিউ ব্লক করা থাকতে পারে"],
            "fake_review_alert": "উচ্চ"
        }
        
    model = genai.GenerativeModel('gemini-pro')
    
    # রিভিউগুলো সাজিয়ে একটি সুনির্দিষ্ট প্রম্পট তৈরি
    prompt = "Analyze the product: " + product_title + "\nReviews:\n" + "\n".join(reviews[:10]) + "\nRespond STRICTLY in JSON: {\"verdict\":\"ভালো/মোটামুটি/এড়িয়ে চলুন\",\"score\":8,\"pros\":[],\"cons\":[],\"fake_review_alert\":\"কম/মাঝারি/বেশি\"}"
    
    try:
        response = model.generate_content(prompt)
        # ক্লিনআপ রেসপন্স যেন JSON পার্স করা যায়
        clean_text = response.text.replace("```json", "").replace("
```", "").strip()
        result = json.loads(clean_text)
        return result
    except Exception as e:
        return {
            "verdict": "অ্যানালাইসিস ব্যর্থ হয়েছে",
            "score": 0,
            "pros": [f"ভুল: {str(e)}"],
            "cons": [],
            "fake_review_alert": "অজানা"
        }