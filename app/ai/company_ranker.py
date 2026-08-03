import json

from ai.llm_client import LLMClient


RANK_PROMPT = """
You are an AI Business Development Consultant.

Evaluate whether the company is a good match for the candidate.

Candidate Role:
{role}

Candidate Skills:
{skills}

Candidate Services:
{services}

Company Name:
{title}

Website:
{url}

Description:
{snippet}

Return ONLY valid JSON.

{{
    "relevant": true,
    "score": 85,
    "reason": ""
}}

Scoring Guidelines

90-100
Excellent AI company

75-89
Strong software company

60-74
Technology company with AI potential

40-59
Some relevance

0-39
Not relevant

Return JSON only.
"""


class CompanyRanker:

    def __init__(self):

        self.llm = LLMClient()

        self.ai_keywords = [

            "ai",
            "artificial intelligence",
            "machine learning",
            "deep learning",
            "computer vision",
            "nlp",
            "llm",
            "automation",
            "data science",
            "analytics",
            "software",
            "technology",
            "cloud",
            "digital transformation",
            "saas",
            "enterprise"

        ]

    def keyword_score(self, company, profile):

        score = 0

        text = (
            company.get("company", "") + " " +
            company.get("url", "") + " " +
            company.get("snippet", "")
        ).lower()

        # AI / Technology keywords
        for keyword in self.ai_keywords:

            if keyword in text:
                score += 6

        # Candidate skills
        for skill in profile.get("skills", []):

            if skill.lower() in text:
                score += 8

        # Candidate services
        for service in profile.get("services", []):

            if service.lower() in text:
                score += 10

        return min(score, 100)

    def rank(self, company, profile):

        rule_score = self.keyword_score(company, profile)

        prompt = RANK_PROMPT.format(

            role=profile.get("desired_role", ""),

            skills=", ".join(profile.get("skills", [])),

            services=", ".join(profile.get("services", [])),

            title=company["company"],

            url=company["url"],

            snippet=company.get("snippet", "")

        )

        try:

            response = self.llm.generate(prompt)

            response = response.strip()

            response = response.replace("```json", "")

            response = response.replace("```", "")

            response = response.strip()

            result = json.loads(response)

            llm_score = result.get("score", 0)

            final_score = round((rule_score + llm_score) / 2)

            result["score"] = final_score

            result["relevant"] = final_score >= 60

            return result

        except Exception:

            return {

                "relevant": rule_score >= 60,

                "score": rule_score,

                "reason": "Keyword-based ranking"

            }