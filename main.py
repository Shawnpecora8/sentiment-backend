from fastapi import FastAPI
from pydantic import BaseModel
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from webull import paper_webull
import requests
from typing import List, Dict
import datetime
import os

from sp500_symbols import sp500_symbols

app = FastAPI()
analyzer = SentimentIntensityAnalyzer()
wb = paper_webull()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

class SentimentData(BaseModel):
    symbol: str
    price: float
    avg_score: float
    timestamp: str

@app.get("/sentiment-data", response_model=List[SentimentData])
def get_sp500_sentiment():
    results = []
    for symbol in sp500_symbols[:10]:  # Limit for performance demo
        try:
            # Get quote from Webull
            quote = wb.get_quote(symbol)
            price = quote.get("close", 0)

            # Get sentiment score
            response = requests.get(
                f"http://localhost:10000/sentiment?symbol={symbol}"
            )
            sentiment = response.json()

            results.append({
                "symbol": symbol,
                "price": price,
                "avg_score": sentiment.get("avg_score", 50),
                "timestamp": sentiment.get("timestamp")
            })
        except Exception as e:
            continue
    return results