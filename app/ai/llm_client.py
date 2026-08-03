import re
import time

from openai import OpenAI


class LLMClient:

    def __init__(self):

        self.client = OpenAI(
            base_url="http://127.0.0.1:1234/v1",
            api_key="lm-studio"
        )

        self.model = "qwen2.5-1.5b-instruct"

    def _clean_response(self, text):

        if not text:
            return ""

        text = text.strip()

        # Remove markdown fences
        text = text.replace("```json", "")
        text = text.replace("```text", "")
        text = text.replace("```markdown", "")
        text = text.replace("```", "")

        return text.strip()

    def extract_json(self, text):

        text = self._clean_response(text)

        match = re.search(r"\{.*\}", text, re.DOTALL)

        if match:
            return match.group()

        return text

    def generate(self, prompt):

        start = time.time()

        

        for attempt in range(3):

            try:

                response = self.client.chat.completions.create(

                    model=self.model,

                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],

                    temperature=0.2,

                    max_tokens=2048,

                    timeout=300
                )

                elapsed = time.time() - start

                print(f"\nLLM Time: {elapsed:.2f} seconds")

                content = response.choices[0].message.content

                if content is None:
                    return ""

                return self._clean_response(content)

            except Exception as e:

                print(f"\nAttempt {attempt + 1} failed")
                print(e)

                if attempt < 2:
                    time.sleep(2)

        return ""