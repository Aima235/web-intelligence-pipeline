import re


class WebsiteParser:

    def __init__(self):

        pass

    def clean_text(self, text):

        if not text:
            return ""

        # Remove excessive blank lines
        text = re.sub(r"\n{2,}", "\n\n", text)

        # Remove repeated spaces
        text = re.sub(r"[ \t]+", " ", text)

        return text.strip()

    def parse(self, crawl_result):

        if crawl_result is None:
            return None

        metadata = crawl_result.metadata or {}

        markdown = self.clean_text(
            crawl_result.markdown
        )

        return {

            "url": crawl_result.url,

            "title": metadata.get(
                "title",
                ""
            ),

            "markdown": markdown,

            "html": crawl_result.html

        }