from urllib.parse import urlparse


class CompanyFinder:

    def __init__(self):

        self.blocked_domains = {

            "linkedin.com",
            "facebook.com",
            "instagram.com",
            "twitter.com",
            "x.com",
            "youtube.com",
            "reddit.com",
            "github.com",
            "stackoverflow.com",
            "wikipedia.org",
            "medium.com",
            "forbes.com",
            "g2.com",
            "goodfirms.co",
            "clutch.co",
            "sortlist.com",
            "designrush.com",
            "crunchbase.com",
            "glassdoor.com",
            "indeed.com",
            "monster.com",
            "ziprecruiter.com",
            "wellfound.com",
            "angel.co",
            "topdevelopers.co",
            "gartner.com",
            "bing.com",
            "google.com"

        }

        self.bad_paths = {

            "/blog",
            "/blogs",
            "/news",
            "/article",
            "/articles",
            "/posts",
            "/stories",
            "/insights",
            "/case-study",
            "/case-studies",
            "/pricing",
            "/support",
            "/docs",
            "/documentation",
            "/community",
            "/forum",
            "/forums",
            "/careers",
            "/jobs",
            "/job",
            "/vacancies",
            "/privacy",
            "/terms",
            "/contact",
            "/login",
            "/signup",
            "/register",
            "/events",
            "/webinar",
            "/press",
            "/media"

        }

        self.ai_keywords = [

            "ai",
            "artificial",
            "machine",
            "learning",
            "deep",
            "computer",
            "vision",
            "nlp",
            "automation",
            "robotics",
            "analytics",
            "software",
            "technology",
            "digital",
            "cloud",
            "data"

        ]

    def calculate_score(self, title, url):

        score = 0

        text = f"{title} {url}".lower()

        for keyword in self.ai_keywords:

            if keyword in text:
                score += 10

        if url.endswith(".com"):
            score += 15

        if url.endswith(".ai"):
            score += 20

        if url.endswith(".io"):
            score += 15

        if url.endswith(".tech"):
            score += 15

        return score

    def filter(self, search_results):

        companies = []

        visited_domains = set()

        for result in search_results:

            url = result.get("url", "")

            if not url:
                continue

            parsed = urlparse(url)

            domain = parsed.netloc.lower().replace("www.", "")

            path = parsed.path.lower()

            if any(site in domain for site in self.blocked_domains):
                continue

            if any(bad in path for bad in self.bad_paths):
                continue

            if domain in visited_domains:
                continue

            visited_domains.add(domain)

            company = {

                "company": result.get("title", domain),

                "domain": domain,

                "url": url,

                "score": self.calculate_score(
                    result.get("title", ""),
                    url
                )

            }

            companies.append(company)

        companies.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        print(f"\nFiltered {len(companies)} high-quality company websites.\n")

        return companies