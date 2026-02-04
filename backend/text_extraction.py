# backend/text_extraction.py
from typing import List
import re

import requests
from bs4 import BeautifulSoup

"""Fetch the raw HTML of a web page.

Args:
    url (str): The URL to request.

Returns:
    str: The raw HTML content of the response.

Raises:
    requests.HTTPError: For non-2xx responses, `resp.raise_for_status()` will raise.
    requests.RequestException: For other networking issues (timeout, DNS, etc.).
"""
def fetch_article_html(url: str) -> str:
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.text

"""Extract the main textual content from an HTML page.

This function removes script/style elements and concatenates all paragraph
text into a single normalized string suited for NLP processing.

Args:
    html (str): Raw HTML string.

Returns:
    str: Cleaned and whitespace-normalized text extracted from <p> tags.
"""
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
