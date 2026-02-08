CRISIS_WORDS = [
    "suicide", "kill myself", "end my life",
    "self harm", "hurt myself"
]

def is_crisis(text: str) -> bool:
    text = text.lower()
    return any(word in text for word in CRISIS_WORDS)
