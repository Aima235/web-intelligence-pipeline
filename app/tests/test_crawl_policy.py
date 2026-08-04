"""
Unit tests for the Governance Module.
"""

from app.governance.policy_validator import PolicyValidator
from app.governance.crawl_manifest import (
    CrawlManifest,
    CrawlStatus,
)
from app.governance.robots_handler import RobotsHandler
from app.governance.crawl_policy import USER_AGENT


# -----------------------------------------------------
# Domain Validation
# -----------------------------------------------------

def test_allowed_domain():

    assert PolicyValidator.is_allowed_domain(
        "https://o2geeks.com"
    )


def test_subdomain_allowed():

    assert PolicyValidator.is_allowed_domain(
        "https://blog.o2geeks.com"
    )


def test_invalid_domain():

    assert not PolicyValidator.is_allowed_domain(
        "https://facebook.com"
    )


# -----------------------------------------------------
# Page Type Validation
# -----------------------------------------------------

def test_valid_page_type():

    assert PolicyValidator.is_allowed_page_type(
        "about"
    )


def test_invalid_page_type():

    assert not PolicyValidator.is_allowed_page_type(
        "admin"
    )


# -----------------------------------------------------
# Excluded Paths
# -----------------------------------------------------

def test_login_page_blocked():

    assert PolicyValidator.is_excluded_path(
        "https://o2geeks.com/login"
    )


def test_admin_page_blocked():

    assert PolicyValidator.is_excluded_path(
        "https://o2geeks.com/admin"
    )


def test_normal_page_not_blocked():

    assert not PolicyValidator.is_excluded_path(
        "https://o2geeks.com/about"
    )


# -----------------------------------------------------
# Crawl Depth
# -----------------------------------------------------

def test_valid_depth():

    assert PolicyValidator.is_valid_depth(2)


def test_invalid_depth():

    assert not PolicyValidator.is_valid_depth(5)


# -----------------------------------------------------
# Crawl Manifest
# -----------------------------------------------------

def test_manifest_creation():

    manifest = CrawlManifest(
        company="O2Geeks",
        requested_url="https://o2geeks.com",
        discovered_url="https://o2geeks.com",
        page_type="homepage",
        status=CrawlStatus.SUCCESS,
        content_hash="abcdef123456",
    )

    assert manifest.company == "O2Geeks"

    assert manifest.status == CrawlStatus.SUCCESS

    assert manifest.page_type == "homepage"


# -----------------------------------------------------
# Robots Handler
# -----------------------------------------------------

def test_robots_handler_creation():

    handler = RobotsHandler(USER_AGENT)

    assert handler.user_agent == USER_AGENT