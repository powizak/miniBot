import os
import logging
from typing import Any, Dict, Optional
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger("gemini")
logger.setLevel(logging.INFO)

class GeminiAPIError(Exception):
    pass

class GeminiClient:
    BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.critical("GEMINI_API_KEY není nastaven!")
            raise ValueError("GEMINI_API_KEY není nastaven!")

    def _headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json"
        }

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((requests.RequestException, GeminiAPIError))
    )
    def _post(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/{endpoint}?key={self.api_key}"
        try:
            resp = requests.post(url, json=payload, headers=self._headers(), timeout=15)
            if resp.status_code != 200:
                logger.error(f"Chyba Gemini API: {resp.status_code} {resp.text}")
                raise GeminiAPIError(f"Chyba Gemini API: {resp.status_code}")
            return resp.json()
        except Exception as e:
            logger.critical(f"Kritická chyba při komunikaci s Gemini API: {e}")
            raise

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        payload = {
            "contents": [{"parts": [{"text": text}]}]
        }
        # Model pro sentiment: "gemini-pro"
        return self._post("gemini-pro:analyzeSentiment", payload)

    def generate_hypotheses(self, prompt: str) -> Dict[str, Any]:
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        # Model pro generování hypotéz: "gemini-pro"
        return self._post("gemini-pro:generateContent", payload)