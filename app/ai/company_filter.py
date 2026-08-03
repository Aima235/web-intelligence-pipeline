class CompanyFilter:
    
    KEYWORDS = [
        "ai",
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "generative ai",
        "llm",
        "software",
        "software development",
        "custom software",
        "automation",
        "digital transformation",
        "consulting",
        "technology",
        "data",
        "analytics",
        "computer vision",
        "nlp",
        "enterprise",
        "cloud",
        "agentic"
    ]

    def is_relevant(self, company):

        text = " ".join([
            company.get("title", ""),
            company.get("snippet", ""),
            company.get("url", "")
        ]).lower()

        score = 0

        for keyword in self.KEYWORDS:
            if keyword in text:
                score += 10

        return {
            "relevant": score >= 20,
            "score": min(score, 100)
        }