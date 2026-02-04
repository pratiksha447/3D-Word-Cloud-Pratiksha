# backend/nlp.py
from typing import List, Dict

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


def extract_keywords_tfidf(
    text: str,
    max_features: int = 50,
) -> List[Dict[str, float]]:
    """
    Returns a list of {word, weight} sorted by weight desc.
    """
    if not text or len(text.split()) < 5:
        return []

    vectorizer = TfidfVectorizer(
        max_features=max_features,
        stop_words="english",
        ngram_range=(1, 2),
    )
    tfidf_matrix = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.toarray()[0]

    # Normalize scores to [0, 1] for easier visualization
    max_score = float(scores.max()) if scores.size > 0 else 1.0
    if max_score == 0:
        max_score = 1.0
    normalized = scores / max_score

    keywords = [
        {"word": feature_names[i], "weight": float(normalized[i])}
        for i in range(len(feature_names))
    ]

    # Sort by weight descending
    keywords.sort(key=lambda x: x["weight"], reverse=True)
    return keywords
