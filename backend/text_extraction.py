# backend/text_extraction.py
from typing import List
import re

import requests
from bs4 import BeautifulSoup


def fetch_article_html(url: str) -> str:
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.text


def extract_main_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    # Remove script/style tags
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    paragraphs: List[str] = [
        p.get_text(separator=" ", strip=True) for p in soup.find_all("p")
    ]
    text = " ".join(paragraphs)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
