import pytest

from app.crawler.scraper import WebsiteScraper

def test_scraper_initialization():

    scraper = WebsiteScraper()

    assert scraper is not None

    assert scraper.headers is not None

    assert len(scraper.pages) > 0
def test_canonical_url():
    
    scraper = WebsiteScraper()

    url = "https://Example.com/About/"

    canonical = scraper.canonicalize_url(url)

    assert canonical == "https://example.com/About"
from unittest.mock import Mock


def test_validate_html_response():

    scraper = WebsiteScraper()

    response = Mock()

    response.status_code = 200

    response.headers = {
        "Content-Type": "text/html"
    }

    response.text = (
        "<html>"
        + ("Hello World " * 20)
        + "</html>"
    )

    valid, error = scraper.validate_response(response)

    assert valid

    assert error is None
def test_blocked_page():
    
    scraper = WebsiteScraper()

    response = Mock()

    response.status_code = 200

    response.headers = {
        "Content-Type": "text/html"
    }

    response.text = (
        "<html>Access Denied</html>"
    )

    valid, error = scraper.validate_response(response)

    assert not valid

    assert "Blocked" in error
def test_small_response():
    
    scraper = WebsiteScraper()

    response = Mock()

    response.status_code = 200

    response.headers = {
        "Content-Type": "text/html"
    }

    response.text = "Hi"

    valid, error = scraper.validate_response(response)

    assert not valid
def test_detect_javascript():
    
    scraper = WebsiteScraper()

    response = Mock()

    response.headers = {
        "Content-Type": "text/html"
    }

    response.text = """
    <html>

    <div id="root"></div>

    <script src="bundle.js"></script>

    </html>
    """

    page_type = scraper.detect_page_type(response)

    assert page_type == "javascript"
