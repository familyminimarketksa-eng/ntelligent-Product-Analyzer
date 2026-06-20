from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from scraper import scrape_product_data
from ai_analyzer import analyze_reviews_with_ai
import uvicorn
import os

app = FastAPI(title="Intelligent Product Analyzer")

# Frontend থেকে রিকোয়েস্ট অ্যালাউ করার জন্য CORS কনফিগারেশন
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    url: str

@app.post("/api/analyze")
async def analyze_product(payload: AnalyzeRequest):
    if not payload.url:
        raise HTTPException(status_code=400, detail="URL is required")
        
    # Step 1: Scrape Data
    scraped_data = await scrape_product_data(payload.url)
    
    # Step 2: AI Analysis
    analysis_result = await analyze_reviews_with_ai(scraped_data["title"], scraped_data["reviews"])
    
    return {
        "product_title": scraped_data["title"],
        "analysis": analysis_result
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)