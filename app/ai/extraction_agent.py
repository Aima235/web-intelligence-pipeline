import json
import re

from ai.llm_client import LLMClient
from prompts.extraction_prompt import EXTRACTION_PROMPT


class ExtractionAgent:

    def __init__(self):

        self.llm = LLMClient()

    def extract(self, markdown: str):

        MAX_CHARS = 15000

        prompt = EXTRACTION_PROMPT.format(
            content=markdown[:MAX_CHARS]
        )

        response = self.llm.generate(prompt)

        print("✓ Information extracted")

        response = response.strip()

        response = response.replace("```json", "")

        response = response.replace("```", "")

        response = response.strip()

        try:

            return json.loads(response)

        except Exception:

            match = re.search(
                r"\{.*\}",
                response,
                re.DOTALL
            )

            if match:

                try:

                    return json.loads(match.group())

                except Exception:

                    pass

            print("Invalid JSON returned by LLM.")

            return {

                "company_name": "",

                "industry": "",

                "summary": "",

                "services": [],

                "products": [],

                "technologies": [],

                "target_clients": [],

                "business_goals": [],

                "pain_points": [],

                "ai_opportunities": [],

                "emails": [],

                "phones": [],

                "social_links": [],

                "location": "",

                "company_size": "",

                "founded": "",

                "certifications": [],

                "partners": [],

                "careers_page": ""

            }