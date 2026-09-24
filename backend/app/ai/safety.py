"""
AI safety utilities — content filtering and output validation.
"""
import re
from typing import Optional

HARMFUL_PATTERNS = [
    r"\b(how to make|instructions for|steps to make)\s+(bomb|weapon|explosive|poison|drug)",
    r"\b(hack|crack|bypass)\s+(security|password|system)",
    r"\b(self.harm|suicide)\b",
]

_compiled_patterns = [re.compile(p, re.IGNORECASE) for p in HARMFUL_PATTERNS]


def is_safe_input(text: str) -> bool:
    """
    Basic safety check for user input before sending to AI.
    Returns False if harmful content is detected.
    """
    for pattern in _compiled_patterns:
        if pattern.search(text):
            return False
    return True


def sanitize_ai_response(text: str) -> str:
    """
    Remove any accidental leakage of prompt internals or API keys.
    In practice this is a last-resort guard.
    """
    # Remove anything that looks like an API key (long alphanumeric strings)
    text = re.sub(r"\bAIza[0-9A-Za-z\-_]{35}\b", "[REDACTED]", text)
    return text


def truncate_context(text: str, max_chars: int = 4000) -> str:
    """Truncate context text to avoid exceeding token limits."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n\n[Content truncated for brevity...]"
