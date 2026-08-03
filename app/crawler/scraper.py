import asyncio
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin


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

    "/careers"

]

    async def crawl(self, base_url):

        html = ""
        all_text = ""
        title = ""

        visited = set()

        for page in self.pages:

            url = urljoin(base_url, page)

            if url in visited:
                continue

            visited.add(url)

            try:

                print(f"Crawling: {url}")

                response = requests.get(
                    url,
                    headers=self.headers,
                    timeout=15,
                    allow_redirects=True
                )

                if response.status_code != 200:
                    continue

                content_type = response.headers.get(
                    "Content-Type",
                    ""
                )

                if "text/html" not in content_type:
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
                    "iframe"
                ]):
                    tag.decompose()

                text = soup.get_text(
                    separator="\n",
                    strip=True
                )

                if text:
                    all_text += "\n\n" + text

                html += response.text

                await asyncio.sleep(0.5)

            except Exception as e:

                print(f"Skipped {url}: {e}")

        result = CrawlResult(
            base_url,
            html,
            all_text
        )

        result.metadata["title"] = title

        return result