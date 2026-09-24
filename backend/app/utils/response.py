"""
Standardized API response builders.
"""
from typing import Any, Optional

from app.schemas.common import PaginationMeta, PaginatedResponse, SuccessResponse
from app.utils.pagination import compute_total_pages


def success(data: Any, message: str = "Operation successful") -> dict[str, Any]:
    """Build a standard success response dict."""
    return {"success": True, "data": data, "message": message}


def paginated(
    data: list[Any],
    total: int,
    page: int,
    page_size: int,
    message: str = "Operation successful",
) -> dict[str, Any]:
    """Build a standard paginated response dict."""
    return {
        "success": True,
        "data": data,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": compute_total_pages(total, page_size),
        },
        "message": message,
    }
