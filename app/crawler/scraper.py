import asyncio
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin

from governance.policy_validator import PolicyValidator
from governance.robots_handler import RobotsHandler
from governance.crawl_manifest import (
    CrawlManifest,
    CrawlStatus,
)


class CrawlResult:

    def __init__(self, url, html, markdown):
        self.url = url
        self.html = html
        self.markdown = markdown

        self.metadata = {
            "title": ""
        }


class WebsiteScraper:

    def __init__(self):

        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/138.0.0.0 Safari/537.36"
            )
        }

        self.validator = PolicyValidator()

        self.robots = RobotsHandler(
            self.headers["User-Agent"]
        )

        self.manifests = []

        self.pages = [
            "",
            "/about",
            "/services",
            "/solutions",
            "/ai",
            "/machine-learning",
            "/products",
            "/case-studies",
            "/portfolio",
            "/clients",
            "/contact",
            "/careers",
        ]

    async def crawl(self, base_url):

        html = ""
        all_text = ""
        title = ""

        visited = set()

        for page in self.pages:

            url = urljoin(base_url, page)

            if not self.validator.is_allowed_domain(url):
                print(f"Blocked domain: {url}")
                continue

            if self.validator.is_excluded_path(url):
                print(f"Excluded path: {url}")
                continue

            if not self.validator.is_valid_depth(1):
                print(f"Depth exceeded: {url}")
                continue

            if url in visited:
                continue

            visited.add(url)

            try:

                print(f"Crawling: {url}")

                allowed = self.robots.is_allowed(url)

                if not allowed:
                    print(f"Blocked by robots.txt: {url}")
                    continue

                response = requests.get(
                    url,
                    headers=self.headers,
                    timeout=15,
                    allow_redirects=True,
                )

                if response.status_code != 200:
                    print(f"Status Code {response.status_code}: {url}")
                    continue

                content_type = response.headers.get(
                    "Content-Type",
                    ""
                )

                if "text/html" not in content_type:
                    print(f"Skipped non-HTML page: {url}")
                    continue

                soup = BeautifulSoup(
                    response.text,
                    "lxml"
                )

                if not title and soup.title:
                    title = soup.title.get_text(strip=True)

                for tag in soup([
                    "script",
                    "style",
                    "noscript",
                    "svg",
                    "img",
                    "iframe",
                ]):
                    tag.decompose()

                text = soup.get_text(
                    separator="\n",
                    strip=True
                )

                print(f"Extracted {len(text)} characters from {url}")

                if text:
                    all_text += "\n\n" + text

                html += response.text

                manifest = CrawlManifest(
                    company=base_url,
                    requested_url=url,
                    discovered_url=response.url,
                    page_type=page if page else "homepage",
                    status=CrawlStatus.SUCCESS,
                    content_hash=str(hash(response.text)),
                )

                self.manifests.append(manifest)

                await asyncio.sleep(0.5)

            except Exception as e:

                print(f"Skipped {url}: {e}")

        result = CrawlResult(
            base_url,
            html,
            all_text,
        )

        result.manifests = self.manifests
        result.metadata["title"] = title

        return result