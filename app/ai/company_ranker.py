import json

from ai.llm_client import LLMClient

RANK_PROMPT = """
You are an AI Business Development Consultant.

Evaluate whether this company is a good match for the candidate.

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

Scoring Rules

90-100
Excellent AI/ML company actively providing AI products or services.

75-89
Software company with strong AI/ML offerings.

60-74
Technology company where candidate skills strongly apply.

40-59
Technology-related but weak fit.

0-39
Irrelevant company.

Return ONLY valid JSON.

{{
    "relevant": true,
    "score": 85,
    "reason": ""
}}
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
            "predictive analytics",
            "generative ai",
            "vision ai",
            "tensorflow",
            "pytorch",
            "fastapi",
            "python",
            "software",
            "technology",
            "saas",
            "enterprise",
            "cloud"
        ]

    def keyword_score(self, company, profile):

        score = 0

        text = (
            company.get("company", "") + " " +
            company.get("url", "") + " " +
            company.get("snippet", "")
        ).lower()
        url = company.get("url", "").lower()

        if "/blog" in url:
        score -= 40

        if "/top" in url:
         score -= 40

        if "/list" in url:
        score -= 40

        if "/company-lists" in url:
        score -= 40
        # AI keywords
        for keyword in self.ai_keywords:
            if keyword in text:
                score += 8

        # Candidate skills
        for skill in profile.get("skills", []):
            if skill.lower() in text:
                score += 12

        # Candidate services
        for service in profile.get("services", []):
            if service.lower() in text:
                score += 15

        # Desired role
        role = profile.get("desired_role", "").lower()

        if role and role in text:
            score += 20
        score = max(score, 0)
        

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

            response = (
                response.replace("```json", "")
                .replace("```", "")
                .strip()
            )

            result = json.loads(response)

            llm_score = result.get("score", 0)

            # Give higher importance to LLM
            final_score = round(
                (rule_score * 0.30) +
                (llm_score * 0.70)
            )

            result["score"] = final_score

            result["relevant"] = (
                final_score >= 65 or
                llm_score >= 75
            )

            print("\n" + "=" * 70)
            print(company["url"])
            print(f"Rule Score : {rule_score}")
            print(f"LLM Score  : {llm_score}")
            print(f"Final Score: {final_score}")
            print("=" * 70)
            print(result)

            return result

        except Exception as e:

            print("\nRanking Error")
            print(company["url"])
            print(e)

            return {
                "relevant": rule_score >= 65,
                "score": rule_score,
                "reason": "Keyword-based ranking"
            }