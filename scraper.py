import asyncio
from playwright.async_api import async_playwright

async def scrape_product_data(url: str):
    async with async_playwright() as p:
        # Anti-bot ব্লকিং এড়ানোর জন্য user_agent ব্যবহার করা হয়েছে
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        page = await context.new_page()
        
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            # ডাইনামিক কন্টেন্ট লোড হওয়ার জন্য ৩ সেকেন্ড অপেক্ষা
            await asyncio.sleep(3) 
            
            # টাইটেল স্ক্রেপ করা
            title = await page.title()
            
            # সাধারণ কিছু রিভিউ ক্লাসের টেক্সট খোঁজা (দারাজ, আমাজন ইত্যাদির জন্য জেনেরিক সিলেক্টর)
            review_elements = await page.query_selector_all("//div[contains(@class, 'review') or contains(@class, 'comment') or contains(@class, 'content')]")
            
            reviews = []
            for el in review_elements[:15]: # প্রথম ১৫টি রিভিউ নেওয়া হচ্ছে
                text = await el.inner_text()
                if text.strip() and len(text.strip()) > 10:
                    reviews.append(text.strip())
            
            # যদি জেনেরিক সিলেক্টরে না পাওয়া যায়, তবে ব্যাকআপ হিসেবে বডি টেক্সট নেওয়া
            if not reviews:
                body_text = await page.inner_text("body")
                reviews = [body_text[:2000]]
                
            await browser.close()
            return {"title": title, "reviews": reviews}
        except Exception as e:
            await browser.close()
            return {"title": "Unknown Product", "reviews": [], "error": str(e)}