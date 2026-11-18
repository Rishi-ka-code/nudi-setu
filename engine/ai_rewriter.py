# -*- coding: utf-8 -*-
"""
AI Dialect Rewriter:
Integrates Google Gemini API for deep linguistic rewriting of complex,
unseen spoken Kannada dialects into standard textbook Kannada (ಪ್ರಮಾಣ ಕನ್ನಡ).
Provides seamless fallback to the local rule engine if offline or no key is provided.
"""

import json
import os
import re
from typing import Dict, Any, Optional

try:
    import requests
except ImportError:
    requests = None


class AIRewriter:
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-3-flash-preview"):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "")
        self.model_name = model_name

    def is_available(self) -> bool:
        """Returns True if an API key is configured."""
        return bool(self.api_key and self.api_key.strip())

    def rewrite(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Rewrites spoken regional Kannada into standard textbook Kannada using Gemini API.
        Returns None if API is unavailable or call fails (triggering local fallback).
        """
        if not self.is_available() or not text or not text.strip():
            return None

        prompt = f"""
You are an expert Kannada linguistic scholar and lexicographer (ಪ್ರಮಾಣ ಕನ್ನಡ ತಜ್ಞರು).
Rewrite the following everyday regional spoken Kannada sentence into clear, grammatically standard textbook Kannada (ಪ್ರಮಾಣ ಕನ್ನಡ / ಶಿಷ್ಟ ಕನ್ನಡ).

Input Spoken Sentence: "{text.strip()}"

Instructions:
1. Preserve the speaker's intended semantic meaning, politeness register, and tone exactly.
2. Standardize regional dialect forms (North Karnataka, Kalyana Karnataka, Kundagannada, Havyaka, Mysuru-Mandya) to textbook Kannada.
3. Return ONLY a strict JSON object with these exact keys:
{{
  "standard_text": "the standardized textbook Kannada rewrite",
  "detected_region": "North Karnataka / Kalyana Karnataka / Coastal / Uttara Kannada / Mysuru-Mandya / General Spoken",
  "region_name_kn": "ಪ್ರಾಂತ್ಯದ ಹೆಸರು (ಕನ್ನಡದಲ್ಲಿ)",
  "confidence": 0.95,
  "transformations": [
    {{"dialect": "regional word", "standard": "standard word", "type": "category"}}
  ],
  "english_meaning": "English translation of the sentence",
  "explanation": "ಸಂಕ್ಷಿಪ್ತ ವಿವರಣೆ (ಕನ್ನಡದಲ್ಲಿ)"
}}
"""

        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key.strip()}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.1,
                "responseMimeType": "application/json"
            }
        }

        try:
            response = requests.post(endpoint, headers=headers, json=payload, timeout=7)
            if response.status_code == 200:
                data = response.json()
                content = data["candidates"][0]["content"]["parts"][0]["text"]
                # Clean up any potential markdown code block wrappers
                clean_content = re.sub(r"^```(?:json)?\s*", "", content.strip())
                clean_content = re.sub(r"\s*```$", "", clean_content.strip())
                # Parse JSON
                result = json.loads(clean_content)
                result["original_text"] = text.strip()
                result["match_type"] = f"Gemini AI Model ({self.model_name})"
                return result
        except Exception:
            # On any failure (network timeout, invalid key, rate limit), return None to fall back to rule engine
            return None

        return None
