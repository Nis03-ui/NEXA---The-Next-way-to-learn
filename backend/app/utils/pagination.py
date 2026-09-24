"""
Pagination utilities used across all list endpoints.
"""
import math
from dataclasses import dataclass
from typing import TypeVar

from fastapi import Query

T = TypeVar("T")


@dataclass
class PaginationParams:
    """Validated pagination query parameters."""

    page: int
    page_size: int

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


def get_pagination(
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(default=20, ge=1, le=100, description="Items per page"),
) -> PaginationParams:
    """FastAPI dependency that extracts and validates pagination parameters."""
    return PaginationParams(page=page, page_size=page_size)


def compute_total_pages(total: int, page_size: int) -> int:
    """Compute total number of pages from total item count and page size."""
    if page_size <= 0:
        return 0
    return math.ceil(total / page_size)
