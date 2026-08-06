import pytest

from app.processing.content_processor import (
    ContentCleaner,
    DuplicateDetector,
    EvidenceGenerator,
)


def test_content_cleaner():

    cleaner = ContentCleaner()

    parsed_data = {
        "url": "https://example.com",
        "title": "Example",
        "html": """
        <html>
            <header>Header</header>
            <nav>Main Menu</nav>

            <h1>About Us</h1>

            <p>We build AI solutions.</p>

            <footer>Footer</footer>
        </html>
        """,
    }

    result = cleaner.clean(parsed_data)

    assert "Main Menu" not in result["clean_content"]
    assert "Header" not in result["clean_content"]
    assert "Footer" not in result["clean_content"]
    
    assert "We build AI solutions." in result["clean_content"]
    assert "About Us" in result["headings"]


def test_duplicate_detector():

    detector = DuplicateDetector()

    page = {
        "url": "https://example.com",
        "clean_content": "Artificial Intelligence",
    }

    first = detector.check(page)

    second = detector.check(page)

    assert first["is_duplicate"] is False
    assert second["is_duplicate"] is True


def test_hash_generation():

    detector = DuplicateDetector()

    hash1 = detector.generate_hash("hello")
    hash2 = detector.generate_hash("hello")

    assert hash1 == hash2


def test_evidence_generator():

    generator = EvidenceGenerator()

    processed = {
        "url": "https://example.com",
        "title": "Example",
        "clean_content": "Artificial Intelligence helps businesses.",
        "content_hash": "abc123",
    }

    result = generator.create(processed)

    evidence = result["evidence"]

    assert evidence["url"] == "https://example.com"
    assert evidence["page_title"] == "Example"
    assert evidence["content_hash"] == "abc123"
    assert evidence["section"] == "main_content"
    assert evidence["content_version"] == "v1"
    assert evidence["source_reference"] == "https://example.com"