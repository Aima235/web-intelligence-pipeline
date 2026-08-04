"""
Scrapy Settings

Applies the governance policy to Scrapy.
"""

from governance.crawl_policy import (
    USER_AGENT,
    DOWNLOAD_DELAY,
    DOWNLOAD_TIMEOUT,
    RETRY_TIMES,
    CONCURRENT_REQUESTS,
    MAX_CRAWL_DEPTH,
    RESPECT_ROBOTS,
)

# ----------------------------------------------------
# Identification
# ----------------------------------------------------

SCRAPY_SETTINGS = {

    "USER_AGENT": USER_AGENT,

    # ------------------------------------------------
    # Robots.txt
    # ------------------------------------------------

    "ROBOTSTXT_OBEY": RESPECT_ROBOTS,

    # ------------------------------------------------
    # Crawl Speed
    # ------------------------------------------------

    "DOWNLOAD_DELAY": DOWNLOAD_DELAY,

    "CONCURRENT_REQUESTS": CONCURRENT_REQUESTS,

    # ------------------------------------------------
    # Timeout
    # ------------------------------------------------

    "DOWNLOAD_TIMEOUT": DOWNLOAD_TIMEOUT,

    # ------------------------------------------------
    # Retry
    # ------------------------------------------------

    "RETRY_ENABLED": True,

    "RETRY_TIMES": RETRY_TIMES,

    # ------------------------------------------------
    # Crawl Scope
    # ------------------------------------------------

    "DEPTH_LIMIT": MAX_CRAWL_DEPTH,

    # ------------------------------------------------
    # Cookies
    # ------------------------------------------------

    "COOKIES_ENABLED": False,

    # ------------------------------------------------
    # Logging
    # ------------------------------------------------

    "LOG_LEVEL": "INFO",
}