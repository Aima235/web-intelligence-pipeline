from copy import deepcopy

OUTPUT_SCHEMA = {
    "company": {
        "name": "",
        "website": "",
        "industry": "",
        "summary": "",
        "location": ""
    },
    "services": [],
    "technologies": [],
    "target_clients": [],
    "business_goals": [],
    "pain_points": [],
    "business_gaps": [],
    "ai_opportunities": [],
    "candidate_match": {
        "score": 0,
        "matched_skills": [],
        "missing_skills": []
    },
    "recommended_services": [],
    "proposal": {
        "summary": "",
        "content": "",
        "proposal_file": ""
    },
    "cms": {
        "title": "",
        "slug": "",
        "category": "",
        "content": ""
    },
    "lead_generation": {
        "priority": "",
        "lead_score": 0,
        "project_type": "",
        "contact_page": ""
    }
}


def create_output_schema():
    return deepcopy(OUTPUT_SCHEMA)