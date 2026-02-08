import requests

from prompt import SYSTEM_PROMPT
from guardrails import is_crisis
from crisis import CRISIS_RESPONSE

from config import GEMINI_API_KEY


def call_gemini_rest(prompt: str) -> str:
    url = "https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash-lite:generateContent"

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY
    }

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=20
    )

    response.raise_for_status()

    return response.json()["candidates"][0]["content"]["parts"][0]["text"]


def generate_reply(user_message: str):
    if is_crisis(user_message):
        return CRISIS_RESPONSE

    try:
        prompt = SYSTEM_PROMPT + f"\nUser: {user_message}"
        text = call_gemini_rest(prompt)

        return {
            "message": text,
            "escalation": False
        }

    except Exception as e:
        return {
            "message": (
                "I'm here with you. I may not have the right words right now, "
                "but you don't have to face this alone."
            ),
            "escalation": False,
            "error": str(e)
        }
