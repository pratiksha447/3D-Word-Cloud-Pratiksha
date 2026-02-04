from typing import List, Dict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl

from text_extraction import fetch_article_html, extract_main_text
from nlp import extract_keywords_tfidf

from fastapi.middleware.cors import CORSMiddleware

"""Pydantic model representing the request body for the /analyze endpoint.

Attributes:
    url (HttpUrl): The URL of the article to analyze. Pydantic will validate it as a URL.
"""
class AnalyzeRequest(BaseModel):
    url: HttpUrl

"""Represents a single keyword and its weight value returned from analysis.

Attributes:
    word (str): The keyword/token text.
    weight (float): Normalized weight in range [0, 1] used for visualization size/color.
"""
class WordItem(BaseModel):
    word: str
    weight: float

"""Response model for /analyze endpoint containing a list of keywords.

Attributes:
    words (List[WordItem]): The list of extracted keywords with weights.
"""
class AnalyzeResponse(BaseModel):
    words: List[WordItem]


app = FastAPI(title="3D Word Cloud API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""
Health check endpoint that verifies the application is running.

Returns:
    dict: A dictionary containing the health status of the application.
            Returns {"status": "ok"} when the application is healthy.
"""
@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

"""
Analyze an article from a given URL and extract keywords using TF-IDF.

This function fetches the HTML content from the provided URL, extracts the main text,
and performs TF-IDF keyword extraction. The extracted keywords are returned as a list
of word items with their respective scores.

Args:
    req (AnalyzeRequest): Request object containing the URL of the article to analyze.

Returns:
    AnalyzeResponse: Response object containing a list of WordItem objects with extracted
                        keywords and their TF-IDF scores.

Raises:
    HTTPException: Status code 400 if the article HTML cannot be fetched or if there's
                    an error during text extraction.
    HTTPException: Status code 422 if insufficient text is found to perform keyword analysis.

Example:
    >>> req = AnalyzeRequest(url="https://example.com/article")
    >>> response = analyze(req)
    >>> print(response.words)
"""
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
