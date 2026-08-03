import asyncio
import time

from agents.website_crawling_agent import WebsiteCrawlingAgent
from utils.profile_builder import build_candidate_profile
from ai.profile_enhancer import ProfileEnhancer
from utils.dataset_generator import DatasetGenerator


async def main():

    print("=" * 70)
    print("AI Company Discovery & Business Proposal Generation Agent")
    print("=" * 70)

    start_time = time.time()

    # --------------------------------------------------
    # Candidate Profile
    # --------------------------------------------------

    print("\nCandidate Profile Wizard")
    print("-" * 70)

    profile = build_candidate_profile()

    print("\n✓ Candidate profile created successfully.")

    # --------------------------------------------------
    # AI Profile Enhancement
    # --------------------------------------------------

    print("\nEnhancing profile using AI...")

    enhancer = ProfileEnhancer()

    profile = enhancer.enhance(profile)

    print("✓ Profile enhanced successfully.")

    print("\n" + "=" * 70)
    print("AI GENERATED PROFILE")
    print("=" * 70)

    print("\nServices")

    for service in profile.get("services", []):
        print(f"✓ {service}")

    print("\nProjects")

    for project in profile.get("projects", []):
        print(f"✓ {project}")

    print("\nTarget Industries")

    for industry in profile.get("target_industries", []):
        print(f"✓ {industry}")

    print("\nSearch Keywords")

    for keyword in profile.get("search_keywords", []):
        print(f"✓ {keyword}")

    # --------------------------------------------------
    # Initialize Agent
    # --------------------------------------------------

    print("\nInitializing AI Discovery Agent...")

    agent = WebsiteCrawlingAgent(profile)

    # --------------------------------------------------
    # AI Pipeline
    # --------------------------------------------------

    print("\nStarting AI Pipeline...\n")

    print("""
Candidate Profile
        ↓
AI Profile Enhancement
        ↓
Search Query Generation
        ↓
Company Discovery
        ↓
Website Crawling
        ↓
Information Extraction
        ↓
Gap Analysis
        ↓
Skill Matching
        ↓
Proposal Generation
        ↓
Professional PDF + JSON Export
""")

    companies = await agent.run()

    # --------------------------------------------------
    # Generate Market Gap Dataset
    # --------------------------------------------------

    print("\nGenerating structured market dataset...")

    dataset_generator = DatasetGenerator()
    dataset_generator.generate()

    print("✓ Structured dataset generated successfully.")

    # --------------------------------------------------
    # Results
    # --------------------------------------------------

    print("\n" + "=" * 70)
    print("FINAL RESULTS")
    print("=" * 70)

    if not companies:
        print("No suitable companies found.")
        return

    for i, company in enumerate(companies, start=1):

        print("\n" + "-" * 70)
        print(f"Company #{i}")
        print("-" * 70)

        print(f"Company Name      : {company.company_name}")
        print(f"Website           : {company.website}")
        print(f"Industry          : {company.industry}")
        print(f"Match Score       : {company.match_score}%")
        print(f"Priority Level    : {company.priority_level}")

        print("\nMatched Skills")
        print("-" * 20)

        if company.matched_skills:
            for skill in company.matched_skills:
                print(f"✓ {skill}")
        else:
            print("None")

        print("\nMissing Skills")
        print("-" * 20)

        if company.missing_skills:
            for skill in company.missing_skills:
                print(f"• {skill}")
        else:
            print("None")

        print("\nRecommended Services")
        print("-" * 20)

        if company.recommended_services:
            for service in company.recommended_services:
                print(f"• {service}")
        else:
            print("None")

        print("\nAI Analysis")
        print("-" * 20)

        print(company.reasoning)

    execution_time = time.time() - start_time

    print("\n" + "=" * 70)
    print("PROCESS COMPLETED SUCCESSFULLY")
    print("=" * 70)
    print(f"Companies Matched : {len(companies)}")
    print(f"Execution Time    : {execution_time:.2f} seconds")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())