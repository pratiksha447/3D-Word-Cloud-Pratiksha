# backend/nlp.py
from typing import List, Dict

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

"""Extract keywords from a single document using TF-IDF.

This function vectorizes the provided `text` using scikit-learn's
TfidfVectorizer and returns up to `max_features` tokens (unigrams & bigrams)
along with a normalized weight in the range [0, 1]. The list is sorted in
descending order by weight which is convenient for visualizations.

Args:
    text (str): The input document text.
    max_features (int): Maximum number of features to consider from TF-IDF.

Returns:
    List[Dict[str, float]]: List of {"word": token, "weight": normalized_score}.
    Returns an empty list if the input text is too short to analyze.
"""
def extract_keywords_tfidf(
    text: str,
    max_features: int = 50,
) -> List[Dict[str, float]]:
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
