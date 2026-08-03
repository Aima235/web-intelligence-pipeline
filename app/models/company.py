from dataclasses import dataclass, field, asdict
from typing import List
import json


@dataclass
class Company:
    """
    Represents a company discovered during the AI Company Discovery pipeline.
    """

    # =========================
    # Basic Information
    # =========================
    company_name: str
    website: str

    industry: str = ""
    summary: str = ""

    # =========================
    # Extracted Information
    # =========================
    services: List[str] = field(default_factory=list)
    technologies: List[str] = field(default_factory=list)

    ai_opportunities: List[str] = field(default_factory=list)
    pain_points: List[str] = field(default_factory=list)

    emails: List[str] = field(default_factory=list)
    phones: List[str] = field(default_factory=list)

    careers_page: str = ""

    # =========================
    # Gap Analysis
    # =========================
    business_gaps: List[str] = field(default_factory=list)
    ai_solutions: List[str] = field(default_factory=list)
    automation_opportunities: List[str] = field(default_factory=list)

    priority_level: str = ""

    # =========================
    # Skill Matching
    # =========================
    match_score: int = 0

    matched_skills: List[str] = field(default_factory=list)
    missing_skills: List[str] = field(default_factory=list)

    recommended_services: List[str] = field(default_factory=list)

    reasoning: str = ""

    # =========================
    # Proposal
    # =========================
    proposal: str = ""

    # =========================
    # Crawl Information
    # =========================
    crawl_status: str = ""
    content_snippet: str = ""

    # =========================
    # Utility Functions
    # =========================
    def model_dump(self):
        """
        Return the dataclass as a dictionary.
        Compatible with Pydantic's model_dump().
        """
        return asdict(self)

    def model_dump_json(self, indent: int = 2):
        """
        Return the dataclass as a JSON string.
        Compatible with Pydantic's model_dump_json().
        """
        return json.dumps(
            asdict(self),
            indent=indent,
            ensure_ascii=False
        )