import re


class ProfileParser:

    def parse(self, profile_text: str):

        skills = self.extract_skills(profile_text)

        return {
            "profile": profile_text,
            "skills": skills,
            "keywords": skills
        }

    def extract_skills(self, text):

        match = re.search(
            r"Skills:(.*?)(Projects:|Experience:|Interested Services:|Education:|$)",
            text,
            re.IGNORECASE | re.DOTALL
        )

        if not match:
            return []

        skills_text = match.group(1)

        # Split on commas, bullets, pipes, semicolons and newlines
        raw_skills = re.split(
            r",|\n|•|-|\||;",
            skills_text
        )

        skills = []

        for skill in raw_skills:

            skill = skill.strip()

            if not skill:
                continue

            if skill.lower() not in [s.lower() for s in skills]:
                skills.append(skill)

        return skills