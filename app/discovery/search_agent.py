from urllib.parse import urlparse

from ddgs import DDGS


class SearchAgent:

    def __init__(self):

        self.ddgs = DDGS()

        self.blocked_domains = {

            "reddit",
            "github",
            "medium",
            "wikipedia",
            "linkedin",
            "facebook",
            "instagram",
            "twitter",
            "x.com",
            "youtube",
            "glassdoor",
            "indeed",
            "ziprecruiter",
            "monster",
            "forbes",
            "g2",
            "clutch",
            "goodfirms",
            "sortlist",
            "designrush",
            "crunchbase",
            "owler",
            "techcrunch",
            "ycombinator",
            "angel.co",
            "wellfound"

        }

    def clean_url(self, url):

        parsed = urlparse(url)

        domain = parsed.netloc.lower()

        domain = domain.replace("www.", "")

        return domain

    def is_blocked(self, domain):

        return any(
            blocked in domain
            for blocked in self.blocked_domains
        )

    def search(self, queries, max_results=10):

        results = []

        visited_domains = set()

        print("\nSearching the Internet...\n")

        for query in queries:

            print(f"Searching: {query}")

            try:

                search_results = self.ddgs.text(
                    query,
                    max_results=max_results
                )

                for item in search_results:

                    url = item.get("href") or item.get("url")

                    if not url:
                        continue

                    domain = self.clean_url(url)

                    if self.is_blocked(domain):
                        continue

                    if domain in visited_domains:
                        continue

                    if url.endswith(
                        (
                            ".pdf",
                            ".jpg",
                            ".png",
                            ".jpeg",
                            ".gif",
                            ".zip",
                            ".doc",
                            ".docx",
                            ".ppt",
                            ".pptx"
                        )
                    ):
                        continue

                    visited_domains.add(domain)

                    results.append({

                        "title": item.get("title", ""),

                        "url": url,

                        "domain": domain,

                        "snippet": item.get("body", "")

                    })

            except Exception as e:

                print(f"Search Error: {e}")

        print(f"\nDiscovered {len(results)} unique company websites.\n")

        return results