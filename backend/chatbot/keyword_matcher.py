"""
keyword_matcher.py
-------------------
Loads the fitness knowledge base (a set of JSON files) and finds the best
matching topic for a user's message using simple, transparent keyword
scoring. No AI models, embeddings, or external services are used here -
just plain text matching, so the logic is easy to read and extend.
"""

import json
import re
from pathlib import Path

# The knowledge_base folder sits right next to this file.
KNOWLEDGE_BASE_DIR = Path(__file__).parent / "knowledge_base"

# Maps each JSON filename (without extension) to the human-readable
# category name shown to the user as the response's "topic".
CATEGORY_LABELS = {
    "nutrition": "Nutrition",
    "workout": "Workout",
    "recovery": "Recovery",
    "hydration": "Hydration",
    "motivation": "Motivation",
    "sleep": "Sleep",
    "supplements": "Supplements",
    "injury_prevention": "Injury Prevention",
}


def load_knowledge_base() -> list:
    """
    Reads every JSON file in knowledge_base/ and returns one flat list of
    topic dictionaries, each tagged with its source category. Called once
    when the chatbot service module is imported.
    """
    topics = []
    for file_path in sorted(KNOWLEDGE_BASE_DIR.glob("*.json")):
        category = CATEGORY_LABELS.get(file_path.stem, file_path.stem.title())
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for topic in data.get("topics", []):
            topic["category"] = category
            topics.append(topic)
    return topics


def _normalize(text: str) -> str:
    """Lowercases and strips punctuation so matching ignores case/punctuation."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def find_best_match(message: str, topics: list):
    """
    Scores every topic against the user's message and returns the
    highest-scoring topic dict, or None if nothing scores above zero.

    Scoring rule: each keyword that appears as a substring of the
    (normalized) message adds points. Multi-word keywords score higher
    than single words, since a multi-word match is a more specific and
    confident signal of intent (e.g. "how much protein" beats just "how").
    """
    normalized_message = _normalize(message)
    if not normalized_message:
        return None

    best_topic = None
    best_score = 0

    for topic in topics:
        score = 0
        for keyword in topic.get("keywords", []):
            normalized_keyword = _normalize(keyword)
            if not normalized_keyword:
                continue
            if normalized_keyword in normalized_message:
                word_count = len(normalized_keyword.split())
                score += word_count * 2 if word_count > 1 else 1

        if score > best_score:
            best_score = score
            best_topic = topic

    return best_topic if best_score > 0 else None
