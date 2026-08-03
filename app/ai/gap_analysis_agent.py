import json

from ai.llm_client import LLMClient
from prompts.gap_analysis_prompt import GAP_ANALYSIS_PROMPT


class GapAnalysisAgent:

    def __init__(self):

        self.llm = LLMClient()

    def _normalize(self, items):

        if not isinstance(items, list):
            return []

        result = []

        for item in items:

            if isinstance(item, str):
                result.append(item)

            elif isinstance(item, dict):

                result.append(
                    item.get("name", "")
                )

        return [x for x in result if x]

    def analyze(self, company):

        company_json = company.model_dump_json(indent=2)

        prompt = GAP_ANALYSIS_PROMPT.replace(
            "{company}",
            company_json
        )

        response = self.llm.generate(prompt)

        response = response.strip()

        response = response.replace("```json", "")

        response = response.replace("```", "")

        try:

            data = json.loads(response)

            data["business_gaps"] = self._normalize(
                data.get("business_gaps", [])
            )

            data["ai_solutions"] = self._normalize(
                data.get("ai_solutions", [])
            )

            data["automation_opportunities"] = self._normalize(
                data.get("automation_opportunities", [])
            )

            data["quick_wins"] = self._normalize(
                data.get("quick_wins", [])
            )

            data["long_term_opportunities"] = self._normalize(
                data.get("long_term_opportunities", [])
            )

            company.integration_data["business_gaps"] = data["business_gaps"]

            company.integration_data["ai_opportunities"] = data["ai_solutions"]

            company.integration_data["recommended_services"] = data.get(
                "recommended_services",
                []
            )

            company.integration_data["lead_generation"] = {

                "priority": data.get(
                    "priority_level",
                    "Unknown"
                ),

                "lead_score": data.get(
                    "lead_score",
                    0
                ),

                "project_type": data.get(
                    "project_type",
                    ""
                ),

                "contact_page": company.careers_page

            }

            return data

        except Exception:

            return {

                "business_gaps": [],

                "ai_solutions": [],

                "automation_opportunities": [],

                "quick_wins": [],

                "long_term_opportunities": [],

                "recommended_services": [],

                "priority_level": "Unknown",

                "lead_score": 0,

                "project_type": ""

            }