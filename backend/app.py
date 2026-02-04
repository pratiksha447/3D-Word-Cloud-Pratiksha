from typing import List, Dict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl

from text_extraction import fetch_article_html, extract_main_text
from nlp import extract_keywords_tfidf

from fastapi.middleware.cors import CORSMiddleware

class AnalyzeRequest(BaseModel):
    url: HttpUrl


class WordItem(BaseModel):
    word: str
    weight: float


class AnalyzeResponse(BaseModel):
    words: List[WordItem]


app = FastAPI(title="3D Word Cloud API")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest) -> AnalyzeResponse:
    try:
        html = fetch_article_html(req.url)
        text = extract_main_text(html)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch article: {e}")

    keywords: List[Dict[str, float]] = extract_keywords_tfidf(text)
    if not keywords:
        raise HTTPException(status_code=422, detail="Not enough text to analyze")

    return AnalyzeResponse(words=[WordItem(**kw) for kw in keywords])
