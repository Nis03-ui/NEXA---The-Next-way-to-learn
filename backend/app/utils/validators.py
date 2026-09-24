"""
Custom input validators used across schemas and services.
"""
import re
from typing import Optional


PASSWORD_MIN_LENGTH = 8
_EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")


def validate_password_strength(password: str) -> str:
    """
    Validate password meets strength requirements.
    Raises ValueError with a descriptive message on failure.
    """
    if len(password) < PASSWORD_MIN_LENGTH:
        raise ValueError(f"Password must be at least {PASSWORD_MIN_LENGTH} characters")
    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain at least one uppercase letter")
    if not re.search(r"[a-z]", password):
        raise ValueError("Password must contain at least one lowercase letter")
    if not re.search(r"\d", password):
        raise ValueError("Password must contain at least one digit")
    return password


def validate_email_format(email: str) -> str:
    """Basic email format validation."""
    if not _EMAIL_RE.match(email):
        raise ValueError("Invalid email address format")
    return email.lower().strip()


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a user-provided filename.
    Strips path separators and restricts to safe characters.
    """
    # Remove path separators
    filename = re.sub(r"[/\\]", "", filename)
    # Replace dangerous characters
    filename = re.sub(r"[^\w\s\-.]", "", filename)
    # Collapse multiple spaces
    filename = re.sub(r"\s+", "_", filename.strip())
    return filename[:255] if filename else "unnamed"


ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}


def validate_file_extension(filename: str) -> bool:
    """Return True if the file extension is allowed."""
    if "." not in filename:
        return False
    ext = "." + filename.rsplit(".", 1)[-1].lower()
    return ext in ALLOWED_EXTENSIONS
