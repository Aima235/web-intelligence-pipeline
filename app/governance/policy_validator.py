"""
Policy Validator

Validates URLs against the crawl policy before crawling.
"""

from urllib.parse import urlparse

from governance.crawl_policy import (
    ALLOWED_PAGE_TYPES,
    EXCLUDED_PATHS,
    MAX_CRAWL_DEPTH,
)


class PolicyValidator:
    """Validates crawl requests against governance rules."""

    @staticmethod
    def is_allowed_domain(url: str) -> bool:
        """
        Allow any valid HTTP/HTTPS website discovered by the search agent.

        We no longer restrict crawling to only o2geeks.com.
        """

        parsed = urlparse(url)

        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.netloc)
        )

    @staticmethod
    def is_allowed_page_type(page_type: str) -> bool:
        """
        Check if page type is allowed.
        """

        return page_type.lower() in ALLOWED_PAGE_TYPES

    @staticmethod
    def is_excluded_path(url: str) -> bool:
        """
        Check if URL contains excluded paths.
        """

        path = urlparse(url).path.lower()

        return any(
            excluded in path
            for excluded in EXCLUDED_PATHS
        )

    @staticmethod
    def is_valid_depth(depth: int) -> bool:
        """
        Validate crawl depth.
        """

        return depth <= MAX_CRAWL_DEPTH