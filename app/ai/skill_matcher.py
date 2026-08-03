from difflib import SequenceMatcher


class SkillMatcher:

    def similarity(self, a, b):
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()

    def match(self, company, profile):

        candidate_skills = [
            s.strip()
            for s in profile["skills"]
        ]

        company_skills = company.technologies

        matched = []
        missing = []

        for tech in company_skills:

            found = False

            for skill in candidate_skills:

                if self.similarity(skill, tech) >= 0.85:
                    matched.append(tech)
                    found = True
                    break

            if not found:
                missing.append(tech)

        if len(company_skills) == 0:
            score = 60
        else:
            score = int(
                len(matched) /
                len(company_skills)
                * 100
            )

        score = max(0, min(score, 100))

        return {
            "match_score": score,
            "matched_skills": matched,
            "missing_skills": missing,
            "recommended_services": company.services[:5],
            "reasoning": (
                f"Matched {len(matched)} of "
                f"{len(company_skills)} required technologies."
            )
        }