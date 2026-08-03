from ai.extraction_agent import ExtractionAgent
from models.company import Company


class InformationExtractor:

    def __init__(self):

        self.agent = ExtractionAgent()

    def extract(self, parsed_data):

        if not parsed_data:
            return None

        content = parsed_data.get("markdown", "").strip()

        if not content:
            return None

        # Limit content sent to the LLM
        content = content[:5000]

        data = self.agent.extract(content)

        if not isinstance(data, dict):
            return None

        company = Company(

            company_name=data.get("company_name", "").strip(),

            website=parsed_data.get("url", "").strip(),

            industry=data.get("industry", "").strip(),

            summary=data.get("summary", "").strip(),

            services=data.get("services", []),

            technologies=data.get("technologies", []),

            ai_opportunities=data.get("ai_opportunities", []),

            pain_points=data.get("pain_points", []),

            emails=data.get("emails", []),

            phones=data.get("phones", []),

            careers_page=data.get("careers_page", "").strip(),

            content_snippet=content[:1200],

            crawl_status="Success"

        )

        # ----------- Additional Information -----------

        company.products = data.get("products", [])

        company.target_clients = data.get("target_clients", [])

        company.business_goals = data.get("business_goals", [])

        company.company_size = data.get("company_size", "")

        company.location = data.get("location", "")

        company.social_links = data.get("social_links", [])

        company.certifications = data.get("certifications", [])

        company.partners = data.get("partners", [])

        company.founded = data.get("founded", "")

        company.integration_data = {

            "company": {

                "name": company.company_name,

                "website": company.website,

                "industry": company.industry,

                "summary": company.summary,

                "location": company.location,

                "company_size": company.company_size,

                "founded": company.founded

            },

            "services": company.services,

            "products": company.products,

            "technologies": company.technologies,

            "target_clients": company.target_clients,

            "business_goals": company.business_goals,

            "pain_points": company.pain_points,

            "business_gaps": [],

            "ai_opportunities": company.ai_opportunities,

            "candidate_match": {},

            "recommended_services": [],

            "proposal": {},

            "cms": {},

            "lead_generation": {},

            "contact": {

                "emails": company.emails,

                "phones": company.phones,

                "social_links": company.social_links

            }

        }

        return company