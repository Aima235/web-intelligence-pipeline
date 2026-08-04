"""
Crawl Manifest Model

Defines the schema for every crawled webpage.
"""

from datetime import datetime, UTC
from enum import Enum
from typing import Optional

from pydantic import BaseModel, HttpUrl, Field


class CrawlStatus(str, Enum):
    """Possible crawl results."""

    SUCCESS = "Success"
    FAILED = "Failed"
    SKIPPED = "Skipped"
    DUPLICATE = "Duplicate"


class ApprovalState(str, Enum):
    """Approval workflow states."""

    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    NEEDS_REVIEW = "Needs Review"


class CrawlManifest(BaseModel):
    """
    Stores metadata for every crawled webpage.
    """

    company: str = Field(..., description="Company name")

    requested_url: HttpUrl = Field(
        ...,
        description="Original URL requested by crawler"
    )

    discovered_url: HttpUrl = Field(
        ...,
        description="Final URL after redirects"
    )

    page_type: str = Field(
        ...,
        description="Homepage, About, Blog, Careers etc."
    )

    status: CrawlStatus

    timestamp: datetime = Field(
    default_factory=lambda: datetime.now(UTC)
)

    content_hash: str = Field(
        ...,
        description="SHA256 hash of page content"
    )

    error: Optional[str] = Field(
        default=None,
        description="Error message if crawl failed"
    )

    approval_state: ApprovalState = ApprovalState.PENDING