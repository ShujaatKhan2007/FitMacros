"""
ai_fallback.py
--------------
An OPTIONAL fallback for questions the free, rule-based knowledge base
(keyword_matcher.py + chatbot_service.py) couldn't answer. This is the
ONLY place in the chatbot that calls an external AI API, and it's only
ever reached after the free rule-based system has already tried and
failed to find a match - see the numbered steps in handle_message().

COST SAFETY - read this before adding your API key:
  - This uses Google's Gemini API free tier. As long as you never add a
    billing account to your Google Cloud project, it is not possible to
    be charged - requests just get blocked once the free daily quota is
    used up, not silently billed.
  - If GEMINI_API_KEY is not set (e.g. you never configure it, or you
    remove it later), this file does nothing and the chatbot silently
    falls back to the original free static message. Nothing breaks.
  - Every call has a short timeout and only fires for genuinely
    unmatched questions - most messages never reach this file at all.
"""

import os
import requests

GEMINI_API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-1.5-flash:generateContent"
)

# Keeps the AI's personality consistent with the rest of the chatbot, and
# repeats the same safety rule the rule-based system already follows.
SYSTEM_INSTRUCTION = (
    "You are the FitMacros Fitness Coach - a friendly, encouraging, "
    "professional fitness and nutrition assistant. Answer the user's "
    "question in a practical, beginner-friendly, educational way, in "
    "under 120 words. Never provide a medical diagnosis - if the "
    "question is about a medical condition, recommend the user consult "
    "a healthcare professional instead of answering directly."
)


def get_ai_reply(message: str, context: dict = None) -> str:
    """
    Calls the Gemini API for a question the rule-based system couldn't
    answer. Returns the AI's reply as a string, or None if the API key
    isn't configured or the request fails for any reason - callers
    should fall back to the static FALLBACK_REPLY in that case.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        # No key configured - this is the normal, expected state unless
        # you've deliberately opted in. Not an error.
        return None

    prompt = SYSTEM_INSTRUCTION + "\n\n"
    if context:
        # Give the AI the same personalized numbers the rule-based system
        # would have access to, so its answer can reference them too.
        prompt += f"The user's calculated nutrition/workout plan: {context}\n\n"
    prompt += f"User's question: {message}"

    try:
        response = requests.post(
            f"{GEMINI_API_URL}?key={api_key}",
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception:
        # Any failure (no internet, quota hit, bad key, unexpected
        # response shape, timeout) - fail quietly. The user still gets a
        # helpful reply from the static fallback, never an error screen.
        return None
