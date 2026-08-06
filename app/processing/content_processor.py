import re
import hashlib
from datetime import datetime
from difflib import SequenceMatcher

from bs4 import BeautifulSoup
from pydantic import BaseModel


class ContentCleaner:
    """
    Cleans crawled HTML content and extracts useful information.
    """

    REMOVE_TAGS = [
        "script",
        "style",
        "noscript",
        "header",
        "footer",
        "nav",
        "aside",
    ]

    def clean(self, parsed_data):
        html = parsed_data.get("html", "") or ""

        soup = BeautifulSoup(html, "html.parser")

        # Remove unwanted HTML elements
        for tag in self.REMOVE_TAGS:
            for element in soup.find_all(tag):
                element.decompose()

        # Remove common cookie/privacy banners
        cookie_patterns = [
            "cookie",
            "privacy",
            "consent",
            "gdpr",
        ]

        for element in soup.find_all(True):
            attrs = " ".join(
                [
                    element.get("id", ""),
                    " ".join(element.get("class", [])),
                ]
            ).lower()

            if any(pattern in attrs for pattern in cookie_patterns):
                element.decompose()

        # Extract headings
        headings = []

        for level in ["h1", "h2", "h3"]:
            for heading in soup.find_all(level):
                text = heading.get_text(" ", strip=True)
                if text:
                    headings.append(text)

        # Extract links
        links = []

        for link in soup.find_all("a", href=True):
            href = link["href"].strip()

            if href:
                links.append(href)

        # Extract visible text
        content = soup.get_text(separator="\n", strip=True)

        # Normalize whitespace
        content = re.sub(r"\n{2,}", "\n", content)
        content = re.sub(r"[ \t]+", " ", content)

        # Remove duplicate paragraphs
        unique = []
        seen = set()

        for line in content.split("\n"):
            line = line.strip()

            if not line:
                continue

            if line not in seen:
                seen.add(line)
                unique.append(line)

        clean_content = "\n".join(unique)

        return {
            **parsed_data,
            "clean_content": clean_content,
            "headings": headings,
            "links": links,
        }


class DuplicateDetector:
    """
    Detects exact and near-duplicate content.
    """

    def __init__(self):
        self.content_store = {}
        self.report = []

    def generate_hash(self, text):
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def similarity(self, text1, text2):
        return SequenceMatcher(None, text1, text2).ratio()

    def check(self, processed_data):

        content = processed_data.get("clean_content", "")
        content_hash = self.generate_hash(content)

        result = {
            "content_hash": content_hash,
            "is_duplicate": False,
            "is_near_duplicate": False,
            "matched_url": None,
            "similarity": 0.0,
        }

        # Exact duplicate
        if content_hash in self.content_store:
            result["is_duplicate"] = True
            result["matched_url"] = self.content_store[content_hash]["url"]

        else:
            # Near duplicate
            for existing in self.content_store.values():
                score = self.similarity(content, existing["content"])

                if score >= 0.90:
                    result["is_near_duplicate"] = True
                    result["matched_url"] = existing["url"]
                    result["similarity"] = round(score, 2)
                    break

            # Store new content
            self.content_store[content_hash] = {
                "url": processed_data["url"],
                "content": content,
            }

        # Add to duplicate report
        self.report.append(
            {
                "url": processed_data["url"],
                "content_hash": content_hash,
                "is_duplicate": result["is_duplicate"],
                "is_near_duplicate": result["is_near_duplicate"],
                "matched_url": result["matched_url"],
                "similarity": result["similarity"],
            }
        )

        return {
            **processed_data,
            **result,
        }

    def get_report(self):
        return self.report


class EvidenceRecord(BaseModel):
    url: str
    page_title: str
    excerpt: str
    retrieval_time: str
    section: str
    content_version: str
    content_hash: str
    source_reference: str


class EvidenceGenerator:

    def create(self, processed_data):

        excerpt = processed_data.get("clean_content", "")[:300]

        evidence = EvidenceRecord(
            url=processed_data.get("url", ""),
            page_title=processed_data.get("title", ""),
            excerpt=excerpt,
            retrieval_time=datetime.now().isoformat(),
            section="main_content",
            content_version="v1",
            content_hash=processed_data.get("content_hash", ""),
            source_reference=processed_data.get("url", ""),
        )

        processed_data["evidence"] = evidence.model_dump()
        return processed_data