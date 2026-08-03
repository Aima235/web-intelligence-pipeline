import os
import re


class ReportGenerator:

    def __init__(self):
        os.makedirs("output/reports", exist_ok=True)

    def _safe_filename(self, filename):
        """
        Convert a company name into a Windows-safe filename.
        """
        filename = re.sub(r'[<>:"/\\|?*]', "_", filename)
        filename = re.sub(r"\s+", " ", filename).strip()
        return filename

    def save(self, company):

        safe_name = self._safe_filename(company.company_name)

        path = os.path.join(
            "output",
            "reports",
            f"{safe_name}.txt"
        )

        with open(path, "w", encoding="utf-8") as f:

            f.write(f"Company: {company.company_name}\n")
            f.write(f"Website: {company.website}\n")
            f.write(f"Industry: {company.industry}\n\n")

            f.write(f"Match Score: {company.match_score}%\n")
            f.write(f"Priority: {company.priority_level}\n\n")

            f.write("Matched Skills\n")
            f.write("-------------------------\n")
            for s in company.matched_skills:
                f.write(f"- {s}\n")

            f.write("\nMissing Skills\n")
            f.write("-------------------------\n")
            for s in company.missing_skills:
                f.write(f"- {s}\n")

            f.write("\nRecommended Services\n")
            f.write("-------------------------\n")
            for s in company.recommended_services:
                f.write(f"- {s}\n")

            f.write("\nReasoning\n")
            f.write("-------------------------\n")
            f.write(company.reasoning)

        return path