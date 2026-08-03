MATCHING_PROMPT = """
You are an expert AI Hiring Consultant.

Compare the candidate profile with the company information.

Your task is to determine how well the candidate matches the company.

Return ONLY valid JSON.

Do not include markdown.

Do not include explanations outside the JSON.

All lists must contain plain strings only.

confidence must be one of:

High

Medium

Low

{{
    "match_score": 0,
    "matched_skills": [],
    "missing_skills": [],
    "recommended_services": [],
    "confidence": "",
    "strengths": [],
    "improvement_areas": [],
    "reasoning": ""
}}



==================================================
RULES
==================================================

Use ONLY the information provided.

Do NOT invent technologies.

Do NOT invent skills.

Do NOT invent company requirements.

If the company does not explicitly mention a technology,
do NOT include it in missing_skills.

Only compare against technologies, frameworks, AI skills,
programming languages and tools that actually appear inside
Company Information.

==================================================
MATCH SCORE
==================================================

90-100
Candidate matches almost every important technology.

80-89
Strong match with only a few missing skills.

70-79
Good match.

50-69
Moderate match.

Below 50
Weak match.

Never return 0 unless there is almost no overlap.

==================================================
MATCHED SKILLS
==================================================

Return every technology that appears in BOTH:

Candidate Profile

AND

Company Information.

Example

Candidate:
Python
FastAPI
TensorFlow

Company:
Python
Docker
TensorFlow

Output

[
    "Python",
    "TensorFlow"
]

==================================================
MISSING SKILLS
==================================================

Return ONLY technologies that

1. appear in Company Information

AND

2. do NOT appear in Candidate Profile.

Example

Company

Python
Docker
AWS
FastAPI

Candidate

Python
FastAPI

Output

[
    "Docker",
    "AWS"
]

Do NOT include:

Python

FastAPI

==================================================
RECOMMENDED SERVICES
==================================================

Recommend services the candidate could deliver using
their existing skills.

Examples

AI Chatbot Development

Computer Vision Solutions

LLM Applications

RAG Systems

Predictive Analytics

AI Automation

NLP Solutions

FastAPI Backend Development

==================================================
REASONING
==================================================

Write 3-5 concise sentences covering:

• Why the candidate is a good fit.

• The strongest matching skills.

• The most important missing skills.

• Which services the candidate could realistically offer this company.

==================================================
COMPANY INFORMATION
==================================================

{company}

==================================================
CANDIDATE PROFILE
==================================================

{profile}

Return ONLY valid JSON.
"""