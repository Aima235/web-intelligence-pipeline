import json

from ai.llm_client import LLMClient
from prompts.proposal_prompt import PROPOSAL_PROMPT


class ProposalAgent:

    def __init__(self):

        self.llm = LLMClient()

    def generate(self, company, profile):

        company_data = company.model_dump_json(indent=2)

        profile_data = json.dumps(
            profile,
            indent=2
        )

        prompt = PROPOSAL_PROMPT.format(
            company=company_data,
            profile=profile_data
        )

        try:

            response = self.llm.generate(prompt)

            response = response.strip()

            response = response.replace(
                "```text",
                ""
            )

            response = response.replace(
                "```",
                ""
            ).strip()

            return response

        except Exception:
            proposal = json.loads(response)
            return proposal
            return """
Business Proposal

We appreciate the opportunity to present this proposal.

Based on the available company information, we believe Artificial Intelligence and intelligent automation can improve operational efficiency, reduce manual work and support future business growth.

Our expertise includes Python, Machine Learning, Deep Learning, Computer Vision, NLP, Large Language Models, FastAPI and modern AI solution development.

We would welcome the opportunity to discuss this proposal further and explore how these solutions can create value for your organization.

Thank you for your time and consideration.
"""