import asyncio
import requests

from bs4 import BeautifulSoup
from urllib.parse import (
    urljoin,
    urlparse,
    urlunparse,
)

from playwright.async_api import async_playwright

from app.governance.policy_validator import PolicyValidator
from app.governance.robots_handler import RobotsHandler
from app.governance.crawl_manifest import (
    CrawlManifest,
    CrawlStatus,
)
import time
from requests.exceptions import (
    Timeout,
    ConnectionError,
    RequestException,
)


class CrawlResult:
    
    def __init__(self, url, html="", markdown=""):
        self.url = url
        self.html = html
        self.markdown = markdown

        self.metadata = {
            "title": "",
            "requested_url": url,
            "final_url": url,
            "canonical_url": url,
            "status_code": None,
            "content_type": "",
            "page_type": "html",
            "response_time": 0.0,
            "redirect_chain": [],
            "redirect_count": 0,
            "used_dynamic": False,
            "success": True,
            "error": None,
        }

        self.manifests = []


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

    def fetch_static(
        self,
        url,
        retries=3,
        timeout=15,
    ):
        """
        Fetch a webpage using requests with retry support.
        """

        last_error = None

        for attempt in range(1, retries + 1):

            try:

                start_time = time.perf_counter()

                response = requests.get(
                    url,
                    headers=self.headers,
                    timeout=timeout,
                    allow_redirects=True,
                )

                response_time = (
                    time.perf_counter() - start_time
                )

                return response, response_time
     
            except (Timeout, ConnectionError) as e:

                last_error = e

                print(
                    f"Retry {attempt}/{retries}: {url}"
                )

                time.sleep(attempt)

            except RequestException as e:

                last_error = e
                break

        raise last_error

    async def fetch_dynamic(self, url):
        """
        Fetch a webpage using Playwright.
        """

        async with async_playwright() as p:

            browser = await p.chromium.launch(headless=True)

            page = await browser.new_page(
                user_agent=self.headers["User-Agent"]
            )

            start_time = time.perf_counter()

            await page.goto(
                url,
                wait_until="networkidle",
                timeout=30000,
            )

            html = await page.content()

            response_time = (
                time.perf_counter() - start_time
            )

            final_url = page.url

            await browser.close()

            return html, final_url, response_time

    def validate_response(self, response):
    
        if response.status_code != 200:
            return False, f"HTTP {response.status_code}"

        content_type = response.headers.get(
            "Content-Type",
            ""
        ).lower()

        if "text/html" not in content_type:
            return False, f"Unsupported content type: {content_type}"

        if not response.text.strip():
            return False, "Empty response"

        blocked_keywords = [
            "access denied",
            "captcha",
            "temporarily unavailable",
            "forbidden",
            "cloudflare",
            "verify you are human",
        ]

        page_text = response.text.lower()

        for keyword in blocked_keywords:
            if keyword in page_text:
                return False, f"Blocked page detected ({keyword})"

        if len(response.text) < 100:
            return False, "Response too small"

        return True, None

    def canonicalize_url(self, url):
        """
        Normalize a URL to avoid duplicate representations.
        """

        parsed = urlparse(url)

        # Remove trailing slash (except root)
        path = parsed.path.rstrip("/")
        if not path:
            path = "/"

        # Remove fragment
        fragment = ""

        # Convert hostname to lowercase
        netloc = parsed.netloc.lower()

        canonical = urlunparse((
            parsed.scheme.lower(),
            netloc,
            path,
            "",
            parsed.query,
            fragment,
        ))

        return canonical

    def detect_page_type(self, response):
        """
        Detect the type of page based on headers and content.
        """

        content_type = response.headers.get(
            "Content-Type",
            ""
        ).lower()

        if "application/pdf" in content_type:
            return "pdf"

        if "application/json" in content_type:
            return "json"

        if "image/" in content_type:
            return "image"

        if "text/xml" in content_type:
            return "xml"

        html = response.text.lower()

        js_indicators = [
            "__next",
            "__nuxt",
            "id=\"root\"",
            "id='root'",
            "id=\"app\"",
            "id='app'",
            "react",
            "angular",
            "vue",
        ]

        text = BeautifulSoup(
            response.text,
            "lxml"
        ).get_text(strip=True)

        if any(indicator in html for indicator in js_indicators):
            if len(text) < 300:
                return "javascript"

        return "html"

    async def crawl(self, base_url):

        html = ""
        all_text = ""
        title = ""

        visited = set()
        used_dynamic = False

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

            canonical_url = self.canonicalize_url(url)
            if canonical_url in visited:
                continue
            visited.add(canonical_url)

            try:

                print(f"Crawling: {url}")

                allowed = self.robots.is_allowed(url)

                if not allowed:
                    print(f"Blocked by robots.txt: {url}")
                    continue

                response, response_time = self.fetch_static(url)

                page_type = self.detect_page_type(response)

                if page_type == "javascript":

                    print(f"Using Playwright: {url}")

                    dynamic_html, final_url, response_time = await self.fetch_dynamic(url)

                    response._content = dynamic_html.encode("utf-8")

                    response.url = final_url

                    used_dynamic = True

                redirect_chain = [
                    r.url for r in response.history
                ]
                redirect_chain.append(response.url)
                redirect_count = len(response.history)
                final_url = response.url
                canonical_url = self.canonicalize_url(final_url)

                valid, error = self.validate_response(response)
                if not valid:
                    print(f"Skipped {url}: {error}")
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
                    page_type=page_type,
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
        result.metadata["requested_url"] = url
        result.metadata["final_url"] = final_url
        result.metadata["canonical_url"] = canonical_url
        result.metadata["redirect_chain"] = redirect_chain
        result.metadata["redirect_count"] = redirect_count
        result.metadata["status_code"] = response.status_code
        result.metadata["content_type"] = response.headers.get(
            "Content-Type",
            ""
        )
        result.metadata["page_type"] = page_type
        result.metadata["used_dynamic"] = used_dynamic
        result.metadata["response_time"] = response_time

        return result