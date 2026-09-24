"""
File upload service using Cloudinary.
Validates file type, MIME type, size, and filename before uploading.
"""
import io
import mimetypes
from typing import Optional

import cloudinary
import cloudinary.uploader
from fastapi import UploadFile

from app.core.config import settings
from app.core.exceptions import FileUploadException
from app.core.logging import get_logger
from app.utils.validators import sanitize_filename, validate_file_extension

logger = get_logger(__name__)

ALLOWED_MIME_TYPES = set(settings.ALLOWED_CONTENT_TYPES)

# Initialize Cloudinary from environment
if settings.CLOUDINARY_URL:
    cloudinary.config(cloudinary_url=settings.CLOUDINARY_URL)
elif settings.CLOUDINARY_CLOUD_NAME:
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
    )


async def upload_file(
    file: UploadFile,
    folder: str = "nexa/materials",
) -> dict[str, str]:
    """
    Validate and upload a file to Cloudinary.

    Args:
        file: The uploaded file from a FastAPI route.
        folder: Cloudinary folder to upload into.

    Returns:
        dict with 'url', 'filename', 'content_type'

    Raises:
        FileUploadException on validation or upload failure.
    """
    # Validate filename
    if not file.filename:
        raise FileUploadException("No filename provided")

    safe_name = sanitize_filename(file.filename)

    if not validate_file_extension(safe_name):
        raise FileUploadException(
            f"File type not allowed. Accepted: PDF, DOCX, TXT"
        )

    # Validate MIME type
    content_type = file.content_type or ""
    if content_type not in ALLOWED_MIME_TYPES:
        # Fallback: guess from extension
        guessed, _ = mimetypes.guess_type(safe_name)
        if guessed not in ALLOWED_MIME_TYPES:
            raise FileUploadException(
                f"Content type '{content_type}' is not allowed"
            )
        content_type = guessed or content_type

    # Validate file size
    contents = await file.read()
    if len(contents) > settings.max_file_size_bytes:
        raise FileUploadException(
            f"File size exceeds maximum allowed size of {settings.MAX_FILE_SIZE_MB} MB"
        )
    if len(contents) == 0:
        raise FileUploadException("File is empty")

    # Upload to Cloudinary
    try:
        result = cloudinary.uploader.upload(
            io.BytesIO(contents),
            folder=folder,
            resource_type="raw",
            public_id=safe_name,
            use_filename=True,
            unique_filename=True,
        )
        url: str = result["secure_url"]
        logger.info("File uploaded", filename=safe_name, url=url[:50])
        return {
            "url": url,
            "filename": safe_name,
            "content_type": content_type,
        }
    except Exception as e:
        logger.error("Cloudinary upload failed", error=str(e), filename=safe_name)
        raise FileUploadException("File upload failed. Please try again.")
