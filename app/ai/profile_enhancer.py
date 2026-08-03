import json

from ai.llm_client import LLMClient


PROFILE_PROMPT = """
You are an AI Career Assistant.

The user has provided:

- Desired Role
- Skills

Your task is to infer:

1. services
2. projects
3. target_industries
4. search_keywords

Return ONLY valid JSON.

{
    "services": [],
    "projects": [],
    "target_industries": [],
    "search_keywords": []
}
"""


class ProfileEnhancer:

    def __init__(self):

        self.llm = LLMClient()

    def enhance(self, profile):

        prompt = f"""
Role:
{profile["desired_role"]}

Skills:
{", ".join(profile["skills"])}

{PROFILE_PROMPT}
"""

        try:

            response = self.llm.generate(prompt)

            response = response.strip()

            response = response.replace("```json", "")
            response = response.replace("```", "")
            response = response.strip()

            enhanced = json.loads(response)

            profile["services"] = enhanced.get("services", [])

            profile["projects"] = enhanced.get("projects", [])

            profile["target_industries"] = enhanced.get(
                "target_industries",
                []
            )

            profile["search_keywords"] = enhanced.get(
                "search_keywords",
                []
            )

        except Exception as e:

            print("Profile Enhancement Error:", e)

            profile.setdefault("services", [])
            profile.setdefault("projects", [])
            profile.setdefault("target_industries", [])
            profile.setdefault("search_keywords", [])

        return profile