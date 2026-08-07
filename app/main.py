import json
import re
import time

from processing.content_processor import (
    ContentCleaner,
    DuplicateDetector,
    EvidenceGenerator,
)

from utils.logger import Logger
from discovery.search_queries import SearchQueryGenerator
from discovery.search_agent import SearchAgent
from discovery.company_finder import CompanyFinder
from utils.report_generator import ReportGenerator
from utils.exporter import Exporter

from crawler.scraper import WebsiteScraper
from crawler.parser import WebsiteParser
from crawler.extractor import InformationExtractor

from ai.company_ranker import CompanyRanker
from ai.gap_analysis_agent import GapAnalysisAgent
from ai.matching_agent import MatchingAgent
from ai.proposal_agent import ProposalAgent

from utils.pdf_generator import PDFGenerator


class WebsiteCrawlingAgent:

    def __init__(self, profile):
        self.profile = profile

        # Discovery
        self.query_generator = SearchQueryGenerator()
        self.search_agent = SearchAgent()
        self.company_finder = CompanyFinder()
        self.report_generator = ReportGenerator()
         
        # Website
        self.scraper = WebsiteScraper()
        self.parser = WebsiteParser()
        self.extractor = InformationExtractor()

        # AI
        self.company_ranker = CompanyRanker()
        self.gap_agent = GapAnalysisAgent()
        self.matching_agent = MatchingAgent()
        self.proposal_agent = ProposalAgent()
        self.logger = Logger()

        # Output
        self.pdf_generator = PDFGenerator()
        self.exporter = Exporter()
        self.evidence_generator = EvidenceGenerator()
        self.content_cleaner = ContentCleaner()
        self.duplicate_detector = DuplicateDetector()

    def clean_filename(self, name):
        if not name:
            return "company"

        return re.sub(r'[\\/*?:"<>|]', "", name).strip()

    async def run(self):
        companies = []
        visited = set()

        start_time = time.time()

        total_found = 0
        relevant_companies = 0
        crawl_success = 0
        extraction_success = 0
        proposal_generated = 0

        self.logger.log("========== NEW RUN STARTED ==========")
        print("\nLoading Candidate Profile...")

        profile = self.profile

        if not profile:
            raise ValueError("Candidate profile was not provided.")

        print("\nCandidate Information")
        print("-" * 50)
        print(f"Name         : {profile.get('name')}")
        print(f"Desired Role : {profile.get('desired_role')}")
        print(f"Location     : {profile.get('location')}")
        print(f"Skills       : {', '.join(profile.get('skills', []))}")

        print("\nGenerating Search Queries...")

        queries = self.query_generator.generate(profile)
        print(f"✓ {len(queries)} queries generated")

        print("\nSearching Internet...")

        search_results = self.search_agent.search(
            queries,
            max_results=10
        )
        print(f"✓ {len(search_results)} websites discovered")

        company_sites = self.company_finder.filter(search_results)

        MAX_TARGET_COMPANIES = 50
        company_sites = company_sites[:MAX_TARGET_COMPANIES]
        total_found = len(company_sites)

        print(f"✓ {len(company_sites)} valid companies found")

        print("\nRanking Companies...")

        ranked = []

        for company_site in company_sites:
            result = self.company_ranker.rank(
                company_site,
                profile
            )
            print("=" * 70)
            print(company_site["url"])
            print(result)

            if result.get("relevant", False):
                company_site["score"] = result.get("score", 0)
                ranked.append(company_site)

        ranked.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        company_sites = ranked[:MAX_TARGET_COMPANIES]
        relevant_companies = len(company_sites)

        print(f"✓ Top {len(company_sites)} companies selected for crawl queue.")

        for index, company_site in enumerate(company_sites, start=1):
            website = company_site["url"]

            bad_domains = [
                "forbes",
                "g2",
                "clutch",
                "goodfirms",
                "sortlist",
                "designrush",
                "reddit",
                "medium",
                "wikipedia",
                "github"
            ]

            if any(domain in website.lower() for domain in bad_domains):
                continue

            if website in visited:
                continue

            visited.add(website)

            print("\n" + "=" * 70)
            print(f"Processing {index}/{len(company_sites)}")
            print(f"Website: {website}")
            self.logger.log(f"Crawling {website}")
            print("=" * 70)

            try:
                crawl_result = await self.scraper.crawl(website)

                if crawl_result is None:
                    print("✕ Crawling failed.")
                    continue

                parsed_page = self.parser.parse(crawl_result)
                crawl_success += 1
             
                if parsed_page is None:
                    print("✕ Parsing failed.")
                    continue

                processed_page = self.content_cleaner.clean(parsed_page)
                processed_page = self.duplicate_detector.check(processed_page)
                processed_page = self.evidence_generator.create(processed_page)

                if not processed_page.get("evidence"):
                    print("✕ Missing evidence. Skipping.")
                    continue

                print(processed_page.get("evidence", ""))

                content_length = len(processed_page.get("markdown", ""))
                print(f"Content Length: {content_length}")

                if content_length < 1000:
                    print("✕ Too little content. Skipping.")
                    continue
                
                markdown = processed_page.get("markdown", "").strip()

                if not markdown:
                    print("✕ Empty cleaned content.")
                    continue
                
                company = self.extractor.extract(processed_page)
                if company is None:
                    print("✕ Extraction failed.")
                    continue

                extraction_success += 1

                if not company.company_name:
                    print("✕ Company name missing.")
                    continue

                print(f"✓ Information extracted for: {company.company_name}")
                self.logger.log(f"Extraction completed: {company.company_name}")

                duplicate = any(
                    c.company_name.lower() == company.company_name.lower()
                    for c in companies
                )

                if duplicate:
                    print("✕ Duplicate company. Skipping.")
                    continue

            except Exception as e:
                print(f"✕ Crawler Error on {website}")
                self.logger.error(website, str(e))
                continue

            # ---------------- GAP ANALYSIS ----------------

            gap = self.gap_agent.analyze(company)

            company.business_gaps = gap.get(
                "business_gaps",
                []
            )

            company.ai_solutions = gap.get(
                "ai_solutions",
                []
            )

            company.automation_opportunities = gap.get(
                "automation_opportunities",
                []
            )

            company.priority_level = gap.get(
                "priority_level",
                "Unknown"
            )

            company.gap_analysis = gap
            print("✓ Gap analysis completed")
            self.logger.log(f"Gap analysis completed: {company.company_name}")

            # ---------------- MATCHING ----------------

            match = self.matching_agent.match(
                company,
                profile
            )

            company.match_score = match.get(
                "match_score",
                0
            )

            company.matched_skills = match.get(
                "matched_skills",
                []
            )

            company.missing_skills = match.get(
                "missing_skills",
                []
            )

            company.recommended_services = match.get(
                "recommended_services",
                []
            )

            company.reasoning = match.get(
                "reasoning",
                ""
            )

            company.matching_result = match
            print("✓ Skill matching completed")
            print(f"✓ Match Score: {company.match_score}%")
            self.logger.log(f"Match Score: {company.company_name} = {company.match_score}%")

            # ---------------- PROPOSAL ----------------

            if (
                match["match_score"] >= 60
                or len(match["matched_skills"]) >= 3
            ):

                proposal = self.proposal_agent.generate(
                    company,
                    profile
                )

                if proposal:

                    filename = self.clean_filename(
                        company.company_name
                    )

                    proposal_path = self.pdf_generator.generate(
                        proposal=proposal,
                        company=company,
                        profile=profile,
                        filename=filename
                    )

                    print(f"✓ Proposal generated and saved: {proposal_path}")
                    proposal_generated += 1

                    self.logger.log(
                        f"Proposal saved for {company.company_name}"
                    )

            else:
                print(
                    "✕ Proposal skipped (match score and matched skills below threshold)"
                )

            # ---------------- EXPORT JSON ----------------
            required = [
                company.company_name,
                company.website,
                company.industry,
            ]

            if not all(required):
                print("✕ Missing required fields.")
                continue
            
            evidence_verified = 0
            evidence_verified += 1
            print(f"Evidence Verified       : {evidence_verified}")
            export_path = self.exporter.export(company)
            print(f"✓ JSON Exported: {export_path}")

            self.logger.log(
                f"JSON exported for {company.company_name}"
            )

            companies.append(company)

            report_path = self.report_generator.save(company)

            print(f"✓ Summary Saved: {report_path}")

        # ---------------- FINAL RESULTS ----------------

        companies.sort(
            key=lambda x: x.match_score,
            reverse=True
        )

        print("\n" + "=" * 70)
        print("BEST MATCHES")
        print("=" * 70)

        for company in companies:
            print(
                f"{company.company_name} | "
                f"{company.website} | "
                f"{company.match_score}%"
            )
            self.logger.log(f"Best match: {company.company_name} with a score of {company.match_score}%")

        self.logger.log("========== RUN FINISHED ==========")

        elapsed = round(time.time() - start_time, 2)

        average_match = 0

        if companies:
            average_match = round(
                sum(c.match_score for c in companies) / len(companies),
                2
            )

        print("\n" + "=" * 70)
        print("RUN SUMMARY")
        print("=" * 70)

        print(f"Companies Found         : {total_found}")
        print(f"Relevant Companies      : {relevant_companies}")
        print(f"Successfully Crawled    : {crawl_success}")
        print(f"Extraction Success      : {extraction_success}")
        print(f"Proposals Generated     : {proposal_generated}")
        print(f"Average Match Score     : {average_match}%")
        print(f"Execution Time          : {elapsed} seconds")

        failed_crawls = total_found - crawl_success
        print(f"Failed Crawls           : {failed_crawls}")
        print(f"Duplicate Companies     : {total_found - len(companies)}")
        print(f"Successful Matches      : {len(companies)}")

        print("=" * 70)

        return companies