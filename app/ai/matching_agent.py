import json
import re
import string

from ai.llm_client import LLMClient
from prompts.matching_prompt import MATCHING_PROMPT


class MatchingAgent:

    TECH_ALIASES = {
        "ml": "machine learning",
        "machine learning": "machine learning",
        "ai": "ai",
        "artificial intelligence": "ai",
        "gen ai": "generative ai",
        "generative ai": "generative ai",
        "llm": "large language models",
        "large language models": "large language models",
        "nlp": "natural language processing",
        "computer vision": "computer vision",
        "cv": "computer vision",
        "tensorflow": "tensorflow",
        "tf": "tensorflow",
        "pytorch": "pytorch",
        "docker": "docker",
        "aws": "aws",
    }

    def __init__(self):
        self.llm = LLMClient()

    def _normalize(self, items):
        if not isinstance(items, list):
            return []

        result = []

        for item in items:
            if isinstance(item, str):
                text = item.strip()
                if text:
                    result.append(text)

            elif isinstance(item, dict):
                name = (
                    item.get("name")
                    or item.get("skill")
                    or item.get("service")
                    or ""
                ).strip()

                if name:
                    result.append(name)

        # Deduplicate while preserving order and casing
        seen = set()
        cleaned = []
        for item in result:
            key = item.lower()
            if key not in seen:
                seen.add(key)
                cleaned.append(item)

        return cleaned

    def _canonical(self, value):
        value = value.lower().strip()
        return self.TECH_ALIASES.get(value, value)

    def _extract_json(self, text):
        if not text:
            return {}

        # Remove markdown block syntax
        text = text.replace("```json", "")
        text = text.replace("```", "").strip()

        # Extract first JSON object
        match = re.search(r"\{.*\}", text, re.DOTALL)

        if not match:
            return {}

        try:
            return json.loads(match.group())
        except Exception:
            return {}

    def match(self, company, profile):
        print("========== FORMAT FIELDS ==========")
        for _, field_name, _, _ in string.Formatter().parse(MATCHING_PROMPT):
            if field_name is not None:
                print(repr(field_name))
        print("===================================")

        prompt = MATCHING_PROMPT.format(
            company=company.model_dump_json(indent=2),
            profile=profile
        )

        response = self.llm.generate(prompt)
        print("\n========== RAW MATCH RESPONSE ==========")
        print(response)
        print("========================================\n")
        data = self._extract_json(response)

        if not data:
            return {
                "match_score": 0,
                "matched_skills": [],
                "missing_skills": [],
                "recommended_services": [],
                "reasoning": "",
                "confidence": "Low"
            }

        # -----------------------
        # Deterministic Score Calculation & Normalization
        # -----------------------
        company_skills = []
        company_skills.extend(company.technologies)
        company_skills.extend(company.services)
        
        candidate = {
            self._canonical(x)
            for x in profile.get("skills", [])
        }
        candidate.update(
            self._canonical(x)
            for x in profile.get("services", [])
        )
        
        company_set = {
            self._canonical(x)
            for x in company_skills
        }
        
        matched = sorted(candidate & company_set)
        missing = sorted(company_set - candidate)
        
        if company_set:
            score = int(len(matched) / len(company_set) * 100)
        else:
            score = 0
            
        score = max(0, min(score, 100))

        # -----------------------
        # Lists Normalization for other fields
        # -----------------------
        recommended = self._normalize(data.get("recommended_services", []))
        reasoning = str(data.get("reasoning", ""))
        confidence = str(data.get("confidence", "Medium"))

        # -----------------------
        # Final Result Object
        # -----------------------
        result = {
            "match_score": score,
            "matched_skills": matched,
            "missing_skills": missing,
            "recommended_services": recommended,
            "confidence": confidence,
            "strengths": self._normalize(data.get("strengths", [])),
            "improvement_areas": self._normalize(data.get("improvement_areas", [])),
            "reasoning": reasoning
        }

        # -----------------------
        # Update Integration Schema
        # -----------------------
        if hasattr(company, "integration_data"):
            company.integration_data["candidate_match"] = {
                "score": score,
                "confidence": confidence,
                "matched_skills": matched,
                "missing_skills": missing,
                "strengths": self._normalize(data.get("strengths", [])),
                "improvement_areas": self._normalize(data.get("improvement_areas", [])),
                "reasoning": reasoning
            }

            company.integration_data["recommended_services"] = recommended

            company.integration_data["candidate_profile"] = {
                "name": profile.get("name", ""),
                "desired_role": profile.get("desired_role", ""),
                "skills": profile.get("skills", []),
                "services": profile.get("services", [])
            }

        return result