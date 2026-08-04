"""
Robots.txt Handler

Checks whether a URL is allowed to be crawled
according to the website's robots.txt.
"""

from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser


class RobotsHandler:
    """Handles robots.txt validation."""

    def __init__(self, user_agent: str):
        self.user_agent = user_agent

    def is_allowed(self, url: str) -> bool:
        """
        Return True if crawling is allowed.
        """

        parsed = urlparse(url)

        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

        parser = RobotFileParser()

        try:
            parser.set_url(robots_url)
            parser.read()

            return parser.can_fetch(
                self.user_agent,
                url
            )

        except Exception:
            # If robots.txt cannot be read,
            # allow crawling instead of blocking.
            return True